lint:
	flake8 bin orgfeeds

install-deps:
	pip install -r dev.txt


.PHONY: lint install-deps
