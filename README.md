# pycaption - iFunny Captions with Python

> With kubinka0505's [iFunny-Captions](https://github.com/kubinka0505/iFunny-Captions) repo being archived for some time, I decided to create a project that has relatively the same functionality.

**pycaption** is meant to recreate the look of iFunny captions (with full emoji support planned), while being simple to use and implement in other projects (either via running from the terminal or importing). It basically just adds a white caption with text above a gif/image.

- [Installation and Usage](#installation-and-usage)
- [Known Issues](#known-issues)

## Example

### Base Gif 
**gifs/silence.gif**\
<img src="gifs/silence.gif" width="180">

---

### Captioning <img src="gifs/hello.gif" align="right" width="180">

`poetry run python3 pycaption -i gifs/silence.gif -o gifs/hello.gif -c 'hello there! 🙂'`

(**gifs/silence.gif** -> **gifs/hello.gif**)

or

```py
from pycaption.caption import caption_gif

caption_gif("gifs/silence.gif", "hello there! 🙂", "gifs/hello.gif")
```


---

### Un-captioning <img src="gifs/silence_again.gif" align="right" width="200">

`poetry run python3 pycaption -i gifs/silence.gif -o gifs/silence_again.gif -u`

(**gifs/hello.gif** -> **gifs/silence_again.gif**)

or

```py
from pycaption.caption import uncaption_gif

uncaption_gif("gifs/silence.gif", "gifs/hello.gif")
```

## Installation and Usage

> **If running from anything other than docker, you may need to install [ImageMagick](https://imagemagick.org/script/download.php) or have the `magick` binary in your `$PATH`.**

### For importing into your own project,  install via pip:
`pip install git+https://github.com/brahdee/pycaption.git`

---

### Manual installation:

You can `git clone` this repo and either:
- Use [python-poetry](https://python-poetry.org/):
    - `poetry install`
    - `poetry run python3 pycaption ...`

- Use [docker](https://www.docker.com/):
    - `docker build . -t pycaption`
    - `docker run -v $PWD/gifs:/pycaption/gifs pycaption -i gifs/... -o gifs/... ...`

        > (change `gifs` in the command to reflect the folder that you want docker to use for input/output)

#### Options:
- `--input | -i [file]` - the path of the gif to use for captioning / uncaptioning
- `--caption | -c [caption ...]` - the text to use for the caption (not needed if using `--uncaption`)
- `--uncaption | -u` (optional) - uncaption the gif instead of captioning it
- `--output | -o [file]` (optional) - the output path of the final result

## More Examples

<img src="https://i.imgur.com/hM8Vtw1.gif" width="200"> <img src="https://i.imgur.com/cXJiUKU.gif" width="200">

## Known Issues
1. **Emojis sometimes display incorrectly** (don't respond well to text wrapping or line spacing), so it's best not to include them in your prompt for now
2. File support hasn't been fully tested (beyond gifs/images) so things may break if using other file formats

---

[MIT License](LICENSE)
