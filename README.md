# DS_visual

A simple program for showing different maps. Currently the supported map types
are standard maps and the Arnold cat maps. Maps are described inside .json
files, so users can write their own map files or edit existing ones. The files
must be in root and are loaded in runtime.

# WARNING

The function expressions inside json files are first parsed with
``parser.expr`` from pythons standard module library and then ``eval``-ed
when drawing new iterations or frames. (inside src/maps.py)

While this is more secure than just running ``eval``, caution is still advised
and I will not be responsible if damage comes from someone using untrusted
sources.

# Requirements
- matplotlib
- numpy
- scipy
- pillow
- PyQt5
- sphinx, for generating documentation.

Sphinx has to be installed via the package manager so that the binaries are
added to the path. Example:
``` shell
apt-get install python3-sphinx
# additionally the third party rtd theme is used
pip3 install sphinx_rtd_theme
```

# Running
The main python file is DS_visual.py
To run it:
``` shell
python3 DS_visual.py
```

# Documentation

There are example images in the images/ directory and a documentation started
in the doc/ directory using Sphinx.

To build the documentation in linux:

``` shell
cd doc
make html
firefox build/html/index.html
```

To build the documentation in windows:
``` shell
cd doc
make.bat html
```
Then open the index.html inside build/html/ with your preffered web browser.
