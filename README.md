# Plancton
Plancton is a [metapost](https://en.wikipedia.org/wiki/MetaPost) font editor.
This is a fork of Luuse’s version over at [GitLab](https://gitlab.com/Luuse/plancton/plancton-editor) making this more comprehensible and accessible for a student workshop @ HAW Hamburg.

## Requirements
If you do not have a package manager already please install one like [Hombrew](https://brew.sh)
 * [Fontforge](http://fontforge.github.io) 
 
To install:
 * [FontForge](https://fontforge.org/)
```brew install fontforge```

 * [Inkscape](https://inkscape.org/)

```brew install inkscape```

 * [TexLive](https://tug.org/texlive/)

```brew install texlive```

 * Python2 or Python3

For example get the latest version [here](https://www.python.org/downloads/)

 * Virtualenv

```brew install virtualenv```

## Install

 * Clone this repository

Proceed with following steps on the command line:
 * `cd plancton-editor` or navigate to whereever you cloned this repository
 * `virtualenv plancton-env`
 * `source plancton-env/bin/activate`
 * `pip install -r requirements.txt`

## Start server

`python plancton-server.py` listening on `http://localhost:8080/`

## Contributors
* [Luuse](http://www.luuse.io/)
* [Simon Thiefes](https://simonthiefes.de)

## License

GNU General Public License - [GPL3](https://www.gnu.org/licenses/gpl-3.0.en.html)


