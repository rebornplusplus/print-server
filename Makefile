# Makefile

VENV = .venv/bin/activate

install:
	@echo "... setting up virtualenv"
	python3 -m venv .venv
	. $(VENV); pip install --upgrade pip
	. $(VENV); pip install --upgrade -r requirements.txt

	@echo "\n" \
		"--------------------------------------------------------------- \n" \
		"* install required packages in virtual env:  make install       \n" \
		"* make and apply migrations:                 make migrate       \n" \
		"* collect static files:                      make collectstatic \n" \
		"* watch, build and serve the django server:  make run           \n" \
		"* run the tests:                             make test          \n" \
		"* clean full environment:                    make clean         \n" \
		"--------------------------------------------------------------- \n"

migrate:
	. $(VENV); python3 manage.py makemigrations accounts
	. $(VENV); python3 manage.py migrate

collectstatic:
	. $(VENV); python3 manage.py collectstatic

run:
	. $(VENV); python3 manage.py runserver

test:
	. $(VENV); python3 manage.py test --verbosity 2

clean:
	rm -rf .venv .static *.sqlite*

all: install migrate collectstatic run test clean

.PHONY: all

