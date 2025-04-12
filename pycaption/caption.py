from utils import EditGif


def _run_func(uncaption: bool, gif_path: str, caption: str, output: str) -> None:
    if not uncaption:
        caption_gif(gif_path, caption, output)
    else:
        uncaption_gif(gif_path, output)


def caption_gif(gif_path: str, caption: str | None, output_path: str | None) -> None:
    if caption is None:
        print("No caption was given, stopping!")
        return

    EditGif(gif_path, output_path).caption(caption)


def uncaption_gif(gif_path: str, output_path: str | None) -> None:
    EditGif(gif_path, output_path).uncaption()
