![](icon_python.svg "PYTHON") [MÉMENTO](../README.md)::Python::XML
==================

## import

```python
import xml.etree.ElementTree as ET
```

Read
----------

We can import this data by reading from a file:
```python
import xml.etree.ElementTree as ET
tree = ET.parse('country_data.xml')
root = tree.getroot()
```

Or directly from a string:

```python
root = ET.fromstring(country_data_as_string)
```

Accesss values
--------------

