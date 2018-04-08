![](icon_python.svg "PYTHON") [MÉMENTO](../../README.md)::Python::VCVARSALL
====================
How to get rid of VCVARSALL error on windows

Symptom
---------
Pip fails to install with the followinf error:
```python
File "c:\python33-b\Lib\distutils\msvc9compiler.py", line 287, in query_vcvarsall raise ValueError(str(list(result.keys())))

ValueError: ['path']
```


The problem
-----------
As I understand, the C++ compiler has to be the same as that used to compile python 3.3. From my research, it seems that the SDK as installed is that same compiler but just doesn't require that the original vcvars64.bat file be present. This information came from [-2-][2]


simple solution
------------------
- go to [http://www.lfd.uci.edu/~gohlke/pythonlibs/#numpy]
- download numpy‑1.9.2+mkl‑cp35‑none‑win_amd64.whl (or other version ccordingly to your setup)
- launch a DOS command prompt
- tpye in :
```dos
pip install path\to\numpy-1.9.2+mkl-cp35-none-win_amd64.whl
```

Et voila !

_Note_ for windows 10 : If you encounter the error below :

    numpy-1.9.1%2Bmkl-cp34-none-win_amd64.whl is not a supported wheel on this platform.

You may check you have admin right permission.


If simple solution failed
-------------------------

Download Visual C++. Note the version of Visual must match the version used to compile python.
- Python 3.4.1 uses MSC v.1600 (Visual Studio C++ 2010)
- Python 2.7, it uses MSC v.1500 (Visual Studio C++ 2008)

Make also sure you __ get the same flavor x86/amd64 __ betwen python and MSVC.

Then, for python 3.4 amd64, do the following:

1) Install Microsoft Visual C++ 2010 Express : [Download Here](https://app.vssps.visualstudio.com/profile/review?download=true&family=VisualStudioCExpress&release=VisualStudio2010)
You'll get an online installer named 'vc_web.exe'.

2) Install Microsoft SDK 7.1 for Windows 7 and .NET Framework 4 [Download Here](http://www.microsoft.com/en-us/download/confirmation.aspx?id=8279)
You'll get an online installer named 'winsdk_web.exe'.

Note : Before installing the Windows SDK v7.1 (these gave me a bad time):
- __ Do not install Microsoft Visual Studio 2010 Service Pack 1 __ yet. If you did then you have to reinstall everything. Uninstalling the Service Pack removes components so you have to reinstall Visual C++ 2010 Express again.
- __ Remove all the Microsoft Visual C++ 2010 Redistributable __ packages from Control Panel\Programs and Features.


3) Create a new vcvars64.bat file under ...\Microsoft Visual Studio 10.0\VC\bin\amd64. Inside of that new batch file I included only the following line:
```sh
CALL "C:\Program Files\Microsoft SDKs\Windows\v7.1\Bin\SetEnv.cmd" /x64
```
I am assuming what this does is forces distutils to use the C++ compiler from the SDK.


Pip installed correctly after this. As I understand, the C++ compiler has to be the same as that used to compile python 3.3. From my research, it seems that the SDK as installed is that same compiler but just doesn't require that the original vcvars64.bat file be present. This information came from [-1-]


References
--------------
[1: vcvarsall-bat-no-64bit-support-vcvars64-bat-missing.6606][1]
[2: python-pip-has-issues-with-path-for-ms-visual-studio-2010-express-for-64-bit-ins][2]

[1]:http://www.w7forums.com/threads/vcvarsall-bat-no-64bit-support-vcvars64-bat-missing.6606
[2]:http://stackoverflow.com/questions/26473854/python-pip-has-issues-with-path-for-ms-visual-studio-2010-express-for-64-bit-ins