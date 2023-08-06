# xaptum-tpm-python

Python wrapper for the xaptum-tpm project

## Requirements
- xaptum-tpm >= 0.4.0

To use a local copy of xaptum-tpm, do the following before building/installing:
```
git clone https://github.com/xaptum/xaptum-tpm
cd xaptum-tpm
mkdir -p build
cd build
cmake ..
cmake --build .
cd ../..
python setup.py addlibpath --xtpm-lib=./xaptum-tpm/build/
```

## Building
```
python setup.py build
```

## Running Tests
The tests assume that a TPM2.0 simulator (for instance, [IBM's simulator](https://sourceforge.net/projects/ibmswtpm2/))
is listening locally on TCP port 2321.

```
pip install -r requirements.txt
python setup.py test
```

## Usage
See the test script at `xaptumtpm/test/test_wrapper.py`
for an example of usage.
