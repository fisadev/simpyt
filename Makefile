build_pyz_in_docker:
	docker run -t -i -v $$(pwd):/code --rm python:3.10 /bin/bash -c "cd /code;rm -rf *.pyz;pip3 install -r requirements_dev.txt;pyempaq ."
	sudo chown $$(whoami):$$(whoami) *.pyz

build_pyz:
	rm -rf *.pyz
	pyempaq .
