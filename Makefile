.PHONY: clean system-packages python-packages install run all

clean:
	find . -type f -name '*.pyc' -delete
	find . -type f -name '*.log' -delete

system-packages:
	sudo apt install python3-pip -y

python-packages:
	sudo pip install -r requirements.txt

install: system-packages python-packages

run:
	python manage.py 

all: clean install run

