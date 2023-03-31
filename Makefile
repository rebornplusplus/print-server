# Makefile

VENV = .venv/bin/activate

install:
	@echo "... setting up virtualenv"
	python3 -m venv .venv
	. $(VENV); pip install --upgrade pip
	. $(VENV); pip install --upgrade -r requirements.txt

	@echo "\n" \
		"--------------------------------------------------------------- \n" \
		"* watch, build and serve the django server:  make run           \n" \
		"* clean full environment:                    make clean         \n" \
		"--------------------------------------------------------------- \n"

run:
	. $(VENV); python3 manage.py runserver

clean:
	rm -rf .venv

all: install run clean

.PHONY: all

