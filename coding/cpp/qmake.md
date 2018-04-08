![](icon_cpp.svg "C++") [MÉMENTO](../../README.md)::CPP::QMAKE
======================

Variables
----------
__Assign__: `VAR = foobar`
Assinged when __qmake__ is run

__retrieve__:

| syntax  		|  scope 				|   time 		|
|---------------|-----------------------|---------------|
|`$$VAR` 		| QMake variable 		| qmake run 	|
|`$${VAR}`		| QMake variable 		| qmake run 	|
|`$(VAR)`		| Environment variable	| Makefile run 	|
|`$$(VAR)`		| Environment variable 	| qmake run 	|

Copy QtDlls
-----------
This is a trick to copy QtDll alongside the executable, allowing to execute it outside QtCreator.

```cpp
win32{
# applys only for windows
CONFIG(debug, debug|release){
    DLL_SUFFIX=d.dll
} else {
    DLL_SUFFIX=.dll
}
# copy QT dll, make sure path are with antislashes
DST_DIR_WIN = $${DESTDIR}
DST_DIR_WIN ~=  s,/,\\,g
SRC_DIR_WIN = $$(QTDIR)\\bin\\

Qt5Core.name = Qt5Core$${DLL_SUFFIX}
Qt5Core.commands = $${QMAKE_COPY} $${SRC_DIR_WIN}$${Qt5Core.name} $${DST_DIR_WIN}\\$${Qt5Core.name}
Qt5Core.target =  $${DESTDIR}/$${Qt5Core.name}

QMAKE_EXTRA_TARGETS += Qt5Core
PRE_TARGETDEPS += $${Qt5Core.target}
} # win32
```

### copy own dlls

```cpp
win32{
	# applys only for windows
    # needs :  $${libFullpath} and $${libFullname} and $${DESTDIR}
    # DLL copy rule
    DLL_COPY_RULE.name = $${libFullname}.dll
    DLL_COPY_RULE.source = $${libFullpath}/$${libFullname}.dll
    DLL_COPY_RULE.target = $${DESTDIR}/$${DLL_COPY_RULE.name}
    DLL_COPY_RULE.commands = $${QMAKE_COPY} $$shell_quote($$shell_path($${DLL_COPY_RULE.source})) $$shell_quote($$shell_path($${DLL_COPY_RULE.target}))
    QMAKE_EXTRA_TARGETS += DLL_COPY_RULE
    POST_TARGETDEPS += $${DLL_COPY_RULE.target}
}
```


##Activate C++11 compilation
```cpp
CONFIG += c++11
```

##Manage build type
In pro file, you can manage different configuration between debug and release.
To active release mode you have to add "CONFIG+=release" in qmqke commande line.

eg : qmake.exe C:\dev\flightManager\flightManager.pro -r -spec win32-g++ "CONFIG+=release"

```cpp
CONFIG(debug, debug|release){
    BUILD_TYPE = debug
    DEFINES += DEBUG
} else {
    BUILD_TYPE = release
    # Add stuff to avoid to open a windows black console when launching flight manager in release mode
    CONFIG += gui windows core
    CONFIG -= console
}
```

Output building directories
-------------------------
```cpp
# define the build root dir
BUILD_DIR   = $${PWD}/build/$${BUILD_TYPE}
# and then the tree
DESTDIR     = $${BUILD_DIR}/bim
OBJECTS_DIR = $${BUILD_DIR}/.obj
MOC_DIR     = $${BUILD_DIR}/.moc
RCC_DIR     = $${BUILD_DIR}/.rcc
UI_DIR      = $${BUILD_DIR}/.ui
```

##Handle version
You can easily manage version in pro file and retrieve this version string in cpp.

```cpp
VERSION = 2.13.0.0
DEFINES += APP_VERSION=\\\"$$VERSION\\\"
```
