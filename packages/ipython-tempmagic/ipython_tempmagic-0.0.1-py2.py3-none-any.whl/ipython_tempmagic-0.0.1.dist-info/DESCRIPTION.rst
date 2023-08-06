# Magics for temporary workspace

- `%cdtemp` -- Creates a temporary directory that is magically cleaned up
  when you exit IPython session.

- `%%with_temp_dir` -- Run Python code in a temporary directory and
  clean up it after the execution.

# Installation

Install using pip:

```
pip install ipython-tempmagic  # PyPI published version
```

or 

```
pip install git+https://github.com/Lightslayer/ipython-tempmagic  # development version
```

For older Jupyter versions (< 5.0):

```text
%install_ext https://raw.github.com/tkf/ipython-tempmagic/master/tempmagic.py
```


