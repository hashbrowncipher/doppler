all: test flakes

test:
	python filtering_utils.py | python zero_detection.py | python alignment.py | python multilateration.py

flakes:
	pyflakes *.py
