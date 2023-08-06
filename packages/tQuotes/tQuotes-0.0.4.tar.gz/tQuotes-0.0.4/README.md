# Tiny Quotes

A small library to get quotes from [GoodReads](https://www.goodreads.com/quotes) and maybe another websites later, maybe not.

To generate a new version of the package, change the version number in the `setup.py` file and run the following commands:

```bash
$ python3 setup.py sdist 
```
```bash
$ twine upload dist/[Filename]
```

## Usage

```bash
pip install tQuotes
```

```python
from quotes import good_reads

message = good_reads.generate_quote()
print(message)
```

**Reference:**
- [Upload a package in pipy using twine](https://anweshadas.in/how-to-upload-a-package-in-pypi-using-twine/)