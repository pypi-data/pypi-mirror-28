*****
:bookmark_tabs: claim
*****

A convenient cli tool that converts file's `carriage returns
<https://en.wikipedia.org/wiki/Carriage_return>`_ to `newlines
<https://en.wikipedia.org/wiki/Newline>`_ or vice versa.

install:
  :code:`pip install claim`

usage:
  :code:`claim [-h] [-dos] filename [filename ...]`

positional arguments:
  :code:`filename`   the file to be converted

optional arguments:
  -h, --help  prompts help message
  -d, -dos    converts file to DOS line endings [\cr\n]

*Note: The files being converted should use UTF-8 encoding, other encodings are currently not supported.*