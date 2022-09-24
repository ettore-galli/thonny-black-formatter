# Build and deploy instructions

https://realpython.com/pypi-publish-python-package/#prepare-your-package-for-publication

## Dependencies
pip-compile pyproject.toml
pip-sync

## Compile and install

### Prerequisites
pip install build twine

### Build
python -m build

### Check build
twine check dist/*

### Test Upload to testpi
twine upload -r testpypi dist/*

### Test Upload to pypi
twine upload dist/*