from PIL import Image
from tempfile import TemporaryDirectory
from subprocess import Popen, PIPE
from io import BytesIO
from pilmoji import Pilmoji
from pilmoji.core import ImageFont
from shlex import split
from math import floor

import numpy
import os
import cv2

FONT_PATH = "./fonts/caption.ttf"
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class EditGif:
    def __init__(self, gif_path: str, output_path: str = None):
        self.full_filename = os.path.basename(gif_path)
        self.filename = self.full_filename.split(".")[0]
        self.extension = self.full_filename.split(".")[-1]
        self.filepath = gif_path

        self.file = Image.open(gif_path)
        self.last_frame = self.file.convert("RGBA")

        self.frames: list[Image.Image] = []
        self.durations: list[int] = []
        self.i = 0

        self.output = output_path

    def _update_progress(self):
        """progress bar that updates on each frame completed"""
        percent = floor(((self.i + 1) / self.file.n_frames) * 100)
        num_full_bars = floor(percent / 10)

        bar = ("❚" * num_full_bars) + (" " * (10 - num_full_bars))

        print(
            f"[{bar}] {percent}%",
            end=("\r" if percent != 100 else " - done! saving...\n"),
        )

    def _next_frame(self):
        """seeks to the next frame in the gif"""
        self.file.seek(self.i)
        self.new_frame = Image.new("RGBA", self.file.size)
        self.new_frame.paste(self.file, (0, 0), self.file.convert("RGBA"))

    def _append_frame(self, image: Image.Image):
        """appends the given frame to a list (along with its duration"""
        self.frames.append(image)
        self.last_frame = self.new_frame
        self.durations.append(self.file.info["duration"])

    def _save(self, prefix: str) -> tuple[BytesIO, str, str]:
        """converts the saved images into a gif byte object"""
        with TemporaryDirectory() as temp:
            cmd = "magick -loop 0 -dispose 2 "

            # save each frame and add them to the command
            for i, (frame, delay) in enumerate(zip(self.frames, self.durations)):
                saved_path = f"{temp}/{i}.png"
                frame.save(saved_path)

                cmd += f"-delay {delay // 10} {saved_path} "

            # read output as bytes
            cmd += " gif:-"

            try:
                p = Popen(split(cmd), stdout=PIPE)
            except FileNotFoundError:
                p = Popen(split(cmd.replace("magick", "convert")), stdout=PIPE)

            result = BytesIO(p.communicate()[0])

        if self.output:
            out = self.output
        else:
            out = f"{self.filename}_{prefix}.{self.extension}"

        with open(out, "wb") as f:
            f.write(result.read())

        return (result, out, "image/gif")

    def _wrap_text(self, font: ImageFont.FreeTypeFont, text: str) -> str:
        """wraps text to fit in a caption"""
        available_width = self.file.size[0] - (self.file.size[0] // 12)
        pre_wrap_lines = text.splitlines()
        wrapped_lines = []

        i = 0
        while i < len(pre_wrap_lines):
            line = pre_wrap_lines[i]
            words = line.split(" ")
            current_line = ""
            word_index = 0

            while word_index < len(words):
                test_line = (current_line + " " + words[word_index]).strip()
                line_width = font.getlength(test_line)

                # compare rendered width with available width
                if line_width <= available_width:
                    current_line = test_line
                    word_index += 1
                else:
                    # splitting long words by character
                    if current_line == "":
                        long_word = words[word_index]
                        split_index = 0
                        partial = ""

                        for j, char in enumerate(long_word):
                            test_partial = partial + char

                            if font.getlength(test_partial + "-") > available_width:
                                break

                            partial = test_partial
                            split_index = j

                        if split_index == 0:
                            split_index = 1
                            partial = long_word[:1]

                        current_line = partial + "-"
                        words[word_index] = long_word[split_index + 1 :]
                    else:
                        break

            wrapped_lines.append(current_line.strip())

            remaining = " ".join(words[word_index:])

            if remaining:
                pre_wrap_lines.insert(i + 1, remaining)

            i += 1

        return "\n".join(wrapped_lines)

    def _create_caption_image(self, text: str):
        """creates the caption image (white background with black text)"""
        width = self.file.size[0]

        spacing = width // 40
        font_size = width // 12
        emoji_scale = 1.2
        emoji_offset = (0, -(font_size // 6))

        # replace ellipsis characters
        text = text.replace("…", "...")

        font = ImageFont.truetype(
            FONT_PATH, font_size, layout_engine=ImageFont.Layout.RAQM
        )

        # wrap caption text
        caption = self._wrap_text(font, text)

        # get the size of the rendered text
        with Pilmoji(Image.new("RGB", (1, 1), WHITE)) as pilmoji:
            rendered_height = pilmoji.getsize(
                text=caption,
                font=font,
                spacing=spacing,
                emoji_scale_factor=emoji_scale,
            )[1]

            text_height = rendered_height + font_size

        caption_img = Image.new("RGB", (width, text_height), WHITE)
        x, y = caption_img.width // 2, caption_img.height // 2

        with Pilmoji(caption_img) as pilmoji:
            pilmoji.text(
                (x, y),
                caption,
                fill=BLACK,
                font=font,
                align="center",
                anchor="mm",
                spacing=spacing,
                emoji_scale_factor=emoji_scale,
                emoji_position_offset=emoji_offset,
            )

        return caption_img

    def _get_content_bounds(self, frame: Image.Image):
        """gets the largest congruent part of the frame without the caption"""
        cv2_image = cv2.cvtColor(numpy.array(frame), cv2.COLOR_RGB2BGR)

        # invert the frame and convert it to grayscale
        img_gray = cv2.cvtColor(cv2.bitwise_not(cv2_image), cv2.COLOR_BGR2GRAY)

        # get morph of grayscale image in order to better separate the caption
        thresh = cv2.threshold(img_gray, 1, 255, cv2.THRESH_BINARY)[1]
        morph_rect = cv2.getStructuringElement(cv2.MORPH_RECT, (15, 15))
        morph = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, morph_rect)

        # finding the largest contour (actual content of the frame)
        largest_area = max(
            cv2.findContours(morph, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[0],
            key=cv2.contourArea,
        )
        _, y, _, _ = cv2.boundingRect(largest_area)

        # part of frame to crop
        bounds = 0, y, cv2_image.shape[1], cv2_image.shape[0]

        return bounds

    def caption(self, text: str):
        """captions the gif"""
        print(f"Captioning {self.filename}.{self.extension} ...")

        caption = self._create_caption_image(text)

        for self.i in range(self.file.n_frames):
            self._next_frame()

            # create image that will contain both caption and original frame
            captioned_frame = Image.new(
                "RGBA", (self.new_frame.width, self.new_frame.height + caption.height)
            )

            # add caption and then original frame under it
            captioned_frame.paste(caption, (0, 0))
            captioned_frame.paste(self.new_frame, (0, caption.height))

            self._append_frame(captioned_frame)
            self._update_progress()

        result = self._save("captioned")
        return result

    def uncaption(self):
        """removes captions from the gif"""
        print(f"Un-captioning {self.filename}.{self.extension} ...")

        self._next_frame()
        bounds = self._get_content_bounds(self.new_frame)

        for self.i in range(self.file.n_frames):
            self._next_frame()
            cropped_frame = self.new_frame.crop(bounds)
            self._append_frame(cropped_frame)
            self._update_progress()

        result = self._save("uncaptioned")
        return result
