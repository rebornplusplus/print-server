# Makefile

.PHONY: help
help:
	@echo "\n" \
		"--------------------------------------------------------------- \n" \
		"* show help:                                 make help          \n" \
		"* install required packages in virtual env:  make install       \n" \
		"* install in clean build environment:        make clean-install \n" \
		"* make and apply migrations:                 make migrate       \n" \
		"* collect static files:                      make collectstatic \n" \
		"* watch, build and serve the django server:  make run           \n" \
		"* run the tests:                             make test          \n" \
		"* clean full environment:                    make clean         \n" \
		"--------------------------------------------------------------- \n"

VENVDIR = .venv
VENV = $(VENVDIR)/bin/activate

.PHONY: venv-setup
venv-setup:
	@echo "... setting up virtualenv"
	python3 -m venv $(VENVDIR)

.PHONY: venv-activate
venv-activate:
	. $(VENV)

.PHONY: install
install: venv-setup venv-activate
	pip install --upgrade pip
	pip install --upgrade -r requirements.txt

.PHONY: clean-install
clean-install: clean install

.PHONY: migrate
migrate: venv-activate
	python3 manage.py makemigrations accounts prints
	python3 manage.py migrate

.PHONY: collectstatic
collectstatic: venv-activate
	python3 manage.py collectstatic

.PHONY: run
run: venv-activate
	python3 manage.py runserver 0.0.0.0:8000

.PHONY: test
test: install venv-activate
	python3 manage.py test --verbosity 2

.PHONY: clean
clean:
	rm -rf $(VENVDIR) .static *.sqlite* .media
