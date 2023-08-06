.PHONY: clean

clean:
	rm -rf *.egg-info
	rm -rf build dist

init:
	pipenv --three
	pipenv install
	pipenv install --dev

uninstall:
	pip uninstall exp-kit

local-install:
	pip install --no-cache-dir dist/exp-kit*.tar.gz

build:
	python setup.py sdist bdist_wheel

test-publish:
	twine upload -r pypitest dist/exp*

test-install:
	pip install --no-cache-dir --index-url https://test.pypi.org/simple/ exp-kit

publish:
	twine upload -r pypi dist/exp*
