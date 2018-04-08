![](icon_python.svg "PYTHON") [MÉMENTO](../../README.md)::Python::pathes
==============

Current working directory
-------------------------

```python
>>> import os
>>> os.getcwd()      # Return the current working directory
'C:\\Python26'
>>> os.chdir('/server/accesslogs')   # Change current working directory
>>> os.system('mkdir today')   # Run the command mkdir in the system shell
```


Constant pathes
---------------
Path of the current script:
```python
SCRIPT_PATH = os.path.realpath(__file__)
```

List files
----------
The folowing will list all files under `root` with filename ending with `.x`
```python
import os
root = "./"
for dirpath, dnames, fnames in os.walk(root):
    for f in fnames:
        if f.endswith(".x"):
            x(os.path.join(dirpath, f))
```

a shorter form would be:
```python
import os
from os.path import join
root = "./"
file_list = [join(p, n) for p, sd, fs in os.walk(root) for n in fs if n.endswith(".x")]
```

Temporary file
-------------------------

```python
import os
from tempfile import mkstemp
temp_file, temp_path = mkstemp()
try: 
	# do what you have to do 
	another_same_file = open(temp_path, 'r')
	data = another_same_file.read()
	another_same_file.close()
finally:
	# clean the mess
	os.close(temp_file)
    os.remove(temp_path)
```



Import path
-----------
```python
import sys
sys.path.insert(0, '/path/to/application/app/folder')

import file
```

os.path functions
------------------

|example|D:\\dev\\perso\\wiki\\md\\python\\path.py|D:\\dev\\perso\\wiki\\md\\python|D:\\dev\\perso\\wiki\\md\\python\\..|
|-------|-------|-------|-------|
|basename|'path.py'|'python'|'..'|
|dirname|'D:\\dev\\perso\\wiki\\md\\python'|'D:\\dev\\perso\\wiki\\md'|'D:\\dev\\perso\\wiki\\md\\python'|
|splitext|('D:\\dev\\perso\\wiki\\md\\python\\path', '.py')|('D:\\dev\\perso\\wiki\\md\\python', '')|('D:\\dev\\perso\\wiki\\md\\python\\..', '')|
|abspath|'D:\\dev\\perso\\wiki\\md\\python\\path.py'|'D:\\dev\\perso\\wiki\\md\\python'|'D:\\dev\\perso\\wiki\\md'|
|abspath|'D:\\dev\\perso\\wiki\\md\\python\\path.py'|'D:\\dev\\perso\\wiki\\md\\python'|'D:\\dev\\perso\\wiki\\md'|
|isfile|True|False|False|
|_isdir|False|True|True|
|isabs|True|True|True|

_______________________________________________
-- Code used to generate this table :
```python
#!/usr/bin/env python3
from os.path import *
funcs = [basename, dirname, splitext, abspath, realpath, isfile, isdir, isabs ]
samples = [
realpath(__file__),
dirname(realpath(__file__)),
join(dirname(realpath(__file__)), '..')
]
table = [[f(sample) for sample in samples] for f in funcs]
# and print it in markdown format
print('|'.join(['', 'example'] + [s.replace('\\', '\\\\') for s in samples] + ['']))
print('|'.join([''] + ['-------'] * (len(samples)+1) + ['']))
for i, l in enumerate(table):
	print('|'.join([''] + [funcs[i].__name__ ] + [p.__repr__() for p in l] + ['']))
```