SHELL := /bin/bash

run:
	python3 -m venv env
	source env/bin/activate  # Set local python environment
	source .env
	pip install -r requirements.txt
	python main.py

show_ip:
	docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' b01673b9677f

drop:
	python drop.py
