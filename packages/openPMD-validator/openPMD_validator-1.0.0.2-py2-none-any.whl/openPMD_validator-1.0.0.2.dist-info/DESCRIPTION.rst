# openPMD Validator Scripts

[![Build Status 1.0.*](https://img.shields.io/travis/openPMD/openPMD-validator/1.0.X.svg?label=1.0.*)](https://travis-ci.org/openPMD/openPMD-validator/branches)
![Supported Python Versions](https://img.shields.io/pypi/pyversions/openPMD-validator.svg)
[![License](https://img.shields.io/badge/license-ISC-blue.svg)](https://opensource.org/licenses/ISC)

This repository contains scripts to validate existing files that (claim to)
implement the [openPMD Standard](https://github.com/openPMD/openPMD-standard)
in version `1.0.*`.

Additional scripts to create random/empty files with the valid markup of the
standard are also provided.


## Rationale

These tools are intended for developers that want to implementent the standard.
They were written to allow an easy *implement-test-correct* workflow without
the hazzle to check every word of the written standard twice.

Nevertheless, these scripts can not validate 100% of the standard and uncovered
sections shall be cross-checked manually with the words of the written
standard.

For more information on requirements for implementations, please refer to the
section
[*Implementations*](https://github.com/openPMD/openPMD-standard/blob/1.0.0/STANDARD.md#implementations)
of the openPMD standard. The repository
  [openPMD-projects](https://github.com/openPMD/openPMD-projects)
also lists a large collection of open source projects that already implement
the openPMD standard.


## Install

[![pypi version](https://img.shields.io/pypi/v/openPMD-validator.svg)](https://pypi.python.org/pypi/openPMD-validator)
[![Spack Package](https://img.shields.io/badge/spack-notyet-yellow.svg)](https://spack.io)
[![Conda Package](https://anaconda.org/ax3l/openpmd_validator/badges/version.svg)](https://anaconda.org/ax3l/openpmd_validator)

### PyPI

```bash
# optional: append --user
pip install openPMD-validator
```

### Spack

*soon*

### Conda

```bash
conda install -c ax3l openpmd_validator
```

## Usage

### CLI

We provide the command-line tools for individual files:

```bash
# optional: create dummy example files
openPMD_createExamples_h5.py

# validate
openPMD_check_h5 -i example.h5
#   optional: append --EDPIC for the Partice-in-Cell Extension
```

### Module

Additionally, the validator tools can be used as *Python module* in your projects, e.g. to verify a file before opening it for reading.

**Create:**
```python
from openpmd_validator import createExamples_h5


# create "example.h5"
createExamples_h5.main()
```

**Check:**
```python
from openpmd_validator import check_h5


result_array = check_h5.check_file("example.h5", verbose=False)

print("Result: %d Errors and %d Warnings."
      %( result_array[0], result_array[1]))
```

## Development

The development of these scripts is carried out *per-branch*.
Each branch corresponds to a certain version of the standard and might
be updated in case tests did contain bugs or we found a way to cover more
sections of the standard.


