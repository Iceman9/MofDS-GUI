# DS_visual

A simple program for showing different maps. Currently the supported map types
are standard maps and the Arnold cat maps. Maps are described inside .json
files, so users can write their own map files or edit existing ones. The files
must be in root and are loaded in runtime.

# WARNING

The function expressions inside json files are first parsed with
``parser.exprs`` from pythons standard module library and then ``eval``-ed
when drawing new iterations or frames. (inside src/maps.py)

While this is more secure than just running ``eval``, caution is still advised
and I will not be responsible if damage comes from someone using untrusted
sources.

# Requirements
- matplotlib
- numpy
- pillow
- PyQt5

# Running
The main python file is DS_visual.py
To run it:
``` shell
python3 DS_visual.py
```

# Documentation

For now in the images/ there are example pictures of the program.