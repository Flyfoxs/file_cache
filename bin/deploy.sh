
#https://packaging.python.org/tutorials/packaging-projects/
rm -rf ./dist/*
#python setup.py register
python setup.py sdist bdist_wheel upload

#python -m twine upload --repository-url https://test.pypi.org/legacy/ dist/*
python -m twine upload dist/*
