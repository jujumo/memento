![](icon_python.svg "PYTHON") [MÉMENTO](../README.md)::Python::re
=========================

### Nota:
`re.match()` checks for a match **only at the beginning** of the string.

Meta-characters
----------------

| pattern           | Description                                                               |
|:------------------|---------------------------------------------------------------------------|
|	`\d` (`\D`)		| Matches any Unicode (not) decimal digit, including [0-9] and many others.	|
| 	`\w` (`\W`)		| Matches Unicode (not) word characters.									|
|	`\s` (`\S`)		| Matches Unicode (not) whitespace characters ([ \t\n\r\f\v] and others		|
|   `.`             | Matches any character except a newline (if not flag DOTALL).              |
|   `^`             | Matches the start of the string.                                          |
|   `$`             | Matches the end of the string or just before the newline.                 |
|   `*`             | Causes the resulting RE to match 0 or more repetitions of the preceding.  |
|   `+`             | Causes the resulting RE to match 1 or more repetitions of the preceding.  |
|   `?`             | Causes the resulting RE to match 0 or 1 repetitions of the preceding.     |
|  `X?`             | Performs the match in non-greedy or minimal fashion. Works with `*`, `+`, `?` and   `{m,n}` |
| `{m}`             | Specifies that exactly m copies of the previous.                          |
| `{m, n}`          | Causes the resulting RE to match from m to n repetitions of the preceding.|
| `{m, n}?`         | Causes the resulting RE to match the fewer from m to n repetitions of the preceding.|
| `\`               | Either escapes special characters                                         |
| `[]`              | Used to indicate a set of characters.										|
|<code>&#124;</code>| match or																	|
| `(...)`           | Matches whatever regular expression is inside the parentheses and indicates the start and end of a group.  |
|`(?aiLmsux)`        | One or more letters from the set 'a', 'i', 'L', 'm', 's', 'u', 'x'.      |
| `(?:...)`          | A non-capturing version of regular parentheses.                          |
| `(?P<name>...)`    | Matches is accessible via the symbolic group name name.                  |
| `(#...)`           | Comment |
| `(?=...)`          | Matches if ... matches next, but doesn’t consume any of the string       |
| `(?!...)`          | Matches if ... doesn’t match next. This is a negative lookahead assertion.|
| `(?<=...)`         | Matches if the current position in the string is preceded by a match for ... that ends at the current position. |

Matching
---------

	match.groupdict(default=None) returns a dictionary containing all the named subgroups.

```python
>>> m = re.match(r"(?P<first_name>\w+) (?P<last_name>\w+)", "Malcolm Reynolds")
>>> m.groupdict()
{'first_name': 'Malcolm', 'last_name': 'Reynolds'}
```