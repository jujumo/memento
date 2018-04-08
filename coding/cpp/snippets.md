![](icon_cpp.svg "C++") [MÉMENTO](../README.md)::CPP::Snippets
==========

Map with default value
-----------------------

Rational: a maps thats returns a default value in case key is not found in the map.

```cpp
#ifndef MAPDEFAULT_HPP
#define MAPDEFAULT_HPP

#include <map>

template<typename K, typename T, T DEFAULT_VALUE>
class MapDefault: public std::map<K, T>
{
public:
    MapDefault()
        : std::map<K, T>()
    {}

    MapDefault(const map<K, T>& base)
        : std::map<K, T>(base)
    {}

    const T& operator[](const K& key) const {
        auto it = find(key);
        if (it==this->end()) {
            static const T DEFAULT = DEFAULT_VALUE;
            return DEFAULT;
        } else {
            return it->second;
        }
    }
};

#endif // MAPDEFAULT_HPP
```
