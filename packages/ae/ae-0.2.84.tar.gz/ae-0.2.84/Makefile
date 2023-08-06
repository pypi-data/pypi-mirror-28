
PYTHON?=python

all: dist crossdist
	ls -1 dist

dist:
	$(PYTHON) setup.py sdist upload
	$(PYTHON) setup.py bdist_wheel upload

crossdist:
	$(PYTHON) cross/fake.py cross/python-2.7-i386 setup.py build --compiler=unix bdist_wheel upload
	$(PYTHON) cross/fake.py cross/python-2.7-amd64 setup.py build --compiler=unix bdist_wheel upload

develop:
	$(PYTHON) setup.py develop

test:
	$(PYTHON) setup.py test

dllinfo:
	for f in `find build/ -iname "*.pyd"` cross/*/python*.dll;  do objdump -p $$f | egrep "DLL Name|file format" | sort; done

clean:
	rm -Rf build dist *.egg-info

.PHONY: test clean info dist crossdist
