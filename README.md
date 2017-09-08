# Python library for FreeIPMI

This is a simple Python library that wraps around FreeIPMI to provide an OO interface.

Pull requests to add additional API features are very welcome. I only implemented what I needed.

## Install
To install it simply issue the following command:

```shell
pip install freeipmi
```

## Documentation
See https://m4ce.github.io/freeipmi-python

## Usage

Below a quick example

```python
>>> from freeipmi import FreeIPMI
>>> ipmi = FreeIPMI()
>>> ipmi.sensors()
```

Handling exceptions:

```python
try:
  ipmi.sensors()
except IPMIError as e:
  print("Exitcode: {0}, Message: {1}".format(e.exitcode, e.message))
```

## Contact

Matteo Cerutti - matteo.cerutti@hotmail.co.uk
