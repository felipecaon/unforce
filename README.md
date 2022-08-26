# About

Unforce - Salesforce recon and exploitation tool*
* Tool under development

The tool is based in python and is currently limited to unix destributions due to path issues.

# Installation

Unforce works with Python 3.

```
$ git clone
$ cd unforce
$ python3 unforce.py -h
```

# Usage

| Arg | Long Arg | Description |
|---|---|---|
| -u | --url | URL to be analyzed by the program, the tool expects the URL with http schema |
| -r | --record | Single salesforce record ID to be queried |

# Output

Every call made by unforce is properly logged inside a snake-case named folder, based on URL used.
Output structure looks like this:

```
example_com_results/
  objects.txt
  csp_sites.txt
  requests/
    User_object.txt
  response/
    User_object.txt
```

# Cache control

To avoid adittional calls Unforce has a cache control system where the fwuid discovered for a salesforce instance is stored.
If the user uses the same URL, the cached fwuid will be used.

Cache is stored in a `.unforce` file inside every results folder.

# Examples


## General recon for a website

```
python3 unforce.py -u https://example.com
``` 

## Querying for a record ID 

```
python3 unforce.py -r 0053k00000ApyN1AAJ
```

# Acknowledgements

🥇 Awesome name by @zeroc00I

