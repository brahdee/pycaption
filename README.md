# pycaption - iFunny Captions with Python

> With kubinka0505's [iFunny-Captions](https://github.com/kubinka0505/iFunny-Captions) repo being archived for some time, I decided to create a project that has relatively the same functionality.

**pycaption** is meant to recreate the look of iFunny captions (with emoji support), while being simple to use and implement in other projects (either via running from the terminal or importing).

- [Installation and Usage](#installation-and-usage)

## Example

### Base Gif 
**gifs/silence.gif**\
<img src="gifs/silence.gif" height="100">

---

### Captioning <img src="gifs/hello.gif" align="right" height="150">

`poetry run python3 pycaption -i gifs/silence.gif -o gifs/hello.gif -c hello there! 🙂`

(**gifs/silence.gif** -> **gifs/hello.gif**)

or

```py
from pycaption.caption import caption_gif

caption_gif("gifs/silence.gif", "hello there! 🙂", "gifs/hello.gif")
```


---

### Uncaptioning <img src="gifs/silence_again.gif" align="right" height="100">

`poetry run python3 pycaption -i gifs/silence.gif -o gifs/silence_again.gif -u`

(**gifs/hello.gif** -> **gifs/silence_again.gif**)

or

```py
from pycaption.caption import uncaption_gif

uncaption_gif("gifs/silence.gif", "gifs/hello.gif")
```

## Installation and Usage

If running from anything other than docker, you may need to install [ImageMagick](https://imagemagick.org/script/download.php) or have the `magick` binary in your `$PATH`.

### Via pip: 
`pip install pycaption`

---

### Manual installation:

You can `git clone` this repo and either:
- Use [python-poetry](https://python-poetry.org/), `poetry install`, and then `poetry run python3 pycaption ...`\
or,
- Use [docker](https://www.docker.com/), `docker build . -t pycaption`, and then `docker run -v $PWD/gifs:/pycaption/gifs pycaption ... -o gifs/...`

#### Options:
- `--input | -i [file]` - the path of the gif to use for captioning / uncaptioning
- `--caption | -c [caption ...]` - the text to use for the caption (not needed if using `--uncaption`)
- (optional) `--uncaption | -u` - uncaption the gif instead of captioning it
- (optional) `--output | -o [file]` - the output path of the final result

<br>

---

[MIT License](LICENSE)
