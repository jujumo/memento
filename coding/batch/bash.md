[MÉMENTO](../README.md)::BASH
=============

pathes
------------

### Script current dir

> Reliable way for a bash script to get the full path to itself  
> -- <cite>[stackoverflow](http://stackoverflow.com/questions/4774054/reliable-way-for-a-bash-script-to-get-the-full-path-to-itself)</cite>

```bash
pushd `dirname $0` > /dev/null
SCRIPTPATH=`pwd -P`
popd > /dev/null
```

### get basename

```bash
$ s=/the/path/foo.txt
$ echo ${s##*/}
foo.txt
$ s=${s##*/}
$ echo ${s%.txt}
foo
$ echo ${s%.*}
foo
```

Arguments
----------

|    |                       description   			 						|
|----|----------------------------------------------------------------------|
| $0 | script name as called.												|
| $* | All parameters as single argument.									|
| $@ | All arguments, one argument per parameter.							|
| $# | Nummber of parameters passés.										|
| $? | Return code of last command.											|
| $$ | PID of shell running script.											|
| $! | PID of last called processus in background.							|

