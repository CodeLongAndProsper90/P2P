.PHONY: release
.PHONY: install
.PHONY: one.py
all: one.py

one.py:
	pyinstaller --onefile --path ~/Python/p2p/env --name Transceiver-dev one.py
release: 
	pyinstaller --onefile --path ~/Python/p2p/env --name Transceiver one.py
install: 
	cp dist/Transceiver-dev /usr/bin/transciver
