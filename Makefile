.PHONY: test
.PHONY: compile
.PHONY: edit
.PHONY: install
	
all: compile

test:
	python3 main.py
compile:
	pyinstaller --name  halibut \
	  --add-data='./assets:./assets'\
	  --add-data='./assets:./assets/*' \
	  --add-data='./parse.py:./parse.py' \
	  --onefile \
	  main.py
	  xz --best -v dist/halibut
edit:
	vim main.py
install:
	cp ./dist/halibut /usr/bin
