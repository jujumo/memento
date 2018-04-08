![](icon_cpp.svg "C++") [MÉMENTO](../README.md)::CPP::RULES
==================
C++ Rule of thumb


Brief
-------

This page talk about : a list of simple practices that every beginner should know.
This page does NOT talk about : coding style, optimizations, naming conventions.
For coding style guidelines, refer to [google cppguide](https://google-styleguide.googlecode.com/svn/trunk/cppguide.html).


Includes order
---------------
Use standard order for readability:
```cpp
// 1. direct linked header
// 2. C system files.
// 3. C++ system files.
// 4. Other libraries' .h files.
// 5. Your project's .h files.
```
and then lexicographic order.

Best practices
-----------------

| practice | severity | Reason |
|----------|----------|--------|
| Always use _header guards_. | stricte | If not defines, and the header is included in multiple files, it leads to redefinition errors. |
| Never ever define _using namespace_ in header. | stricte | Else, it propagates the namepsace to all sources files, leading to unexpected behaviour. |
| Make sure base classes have _virtual destructors_. | stricte | If not defined, inherited destructor may never be called. |
| Always defines _const_ whenever its possible. | strong | Of course for obvious code safety, but more importantly to not forbid its use from other const methods/functions. |
| Consider using smart pointers or auto_ptrs in place of raw pointers | strong | memory leaks are less likely (in which case you don't need a destructor). |
| Consider using std::string (or QString) in place of raw ```char[]``` (or at least use safe version ```strn*()``` ) | strong | less prone to buffer overflows. And buffer overflow is very hard to diagnose. |
| Don't try to return a reference when you must return an object. | strong | avoid the risk to give reference to an object that will soon disappear. |
| Do not use preprocessor macro ```#define``` (prefer static const) | medium | 1) respect scope and 2) type-safe. Example: ```#define square(x) (x*x)``` and used as ```square(d+1)``` leads to ``` (d+(1*d)+1) ``` instead of ```((d+1)*(d+1))``` |
| Prefer non-member non-friend functions to member functions. | medium | cutting dependencies and allowing reuse. |
| Prefer pass-by-reference to pass-by-value. | medium | This is much more efficient: no constructors or destructors are called, because no new objects are being created. |
| Use Pimpl idiom for classes exposed to outside world. | low | The end-user may not bother of youre private data (and its updates). And minimize compilation dependencies between files. |
| Use class declarations instead of class definitions whenever you can. | low | similliar to the later one. |
| for ```#include``` use double quote for files next to the includer, angle brackets for everything else | low | the search rules differs |
| 1 line, 1 instruction | low | 1) easiest to debug (step by step), 2) execution order not always trivial. Example: ```i = 2; division(++i, ++i);``` leads to ```division(2,3)``` or ```division(3,2)``` depending of the compilator. |


