# define the name of the virtual environment directory
VENV := venv

# default target, when make executed without arguments
all: venv

$(VENV)/bin/activate: requirements.txt
	python3 -m venv $(VENV)
	./$(VENV)/bin/pip3 install -r requirements.txt

# init is a shortcut target
init: $(VENV)/bin/activate

run: venv
	./$(VENV)/bin/python3 ./example.py

test: venv
	./$(VENV)/bin/python3 -m pytest

clean:
	rm -rf $(VENV)
	rm -rf ".pytest_cache"

.PHONY: all venv run clean