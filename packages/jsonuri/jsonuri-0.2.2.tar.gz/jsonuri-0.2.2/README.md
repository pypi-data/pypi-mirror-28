
# JSONURI-PY
 
This package helps you convert Python dictionaries into an Gzip compressed, Base64 string for use as a HTTP GET request parameter and reverse it.

An example of a practical application would be to send JSON data over HTTP GET, e.g. to a static resource small.png,
and harvest the data from access logs instead of running real-time data collection.

**Note**: You should avoid sending sensitive information using this mechanism, even if you're doing it over SSL.

## Equivalent libs/packages:

| Language | Repo                                |
|----------|-------------------------------------|
| JavaScript   | https://github.com/guidj/jsonuri-js |


## Examples:


```python
>>> from jsonuri import jsonuri
>>> data = {"age": 31, "name": "John", "account": {"id": 127, "regions": ["US", "SG"]}}
>>> jsonuri.serialize(data, b64_encode=True, uri_encode=False)
'H4sIANRnb1oC/6tWSkxPVbJSMDbUUVDKS8wFsZW88jPylID8xOTk/NK8EqBQtVJmCpAyNDIHChelpmfm5xUD+dFKocEghcHuSrG1tQCN2YKETAAAAA=='
>>> ser = jsonuri.serialize(data, b64_encode=True, uri_encode=True)
'H4sIAOdnb1oC%2F6tWSkxPVbJSMDbUUVDKS8wFsZW88jPylID8xOTk%2FNK8EqBQtVJmCpAyNDIHChelpmfm5xUD%2BdFKocEghcHuSrG1tQCN2YKETAAAAA%3D%3D'
>>> jsonuri.deserialize(ser)
{'age': 31, 'name': 'John', 'account': {'id': 127, 'regions': ['US', 'SG']}}
```
