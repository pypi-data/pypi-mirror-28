all: documentation nightly clean

nightly:
	RELEASE=0 ./setup.py sdist --formats=gztar

release:
	RELEASE=1 ./setup.py sdist --formats=gztar

documentation: doc/help.txt doc/pydoc/stepic.html stepic.1

doc/help.txt: stepic
	./stepic --help > doc/help.txt

doc/pydoc/stepic.html: stepic.py
	pydoc -w stepic
	mkdir -p doc/pydoc/
	mv stepic.html doc/pydoc/

stepic.1: stepic stepic.help2man_include
	help2man --include=stepic.help2man_include --output=stepic.1 ./stepic

clean:
	./setup.py clean
	-rm -rf build MANIFEST
	-find -name "*.py[co]" -print0 | xargs -0 rm

.PHONY: all release documentation clean
