.PHONY: release
.PHONY: install
<<<<<<< HEAD
.PHONY: one.py
all: one.py

one.py:
	pyinstaller --onefile --path env/lib/python3.7/site-packages --name Transceiver-dev one.py
release: 
	pyinstaller --onefile --path env/lib/python3.7/site-packages --name Transceiver one.py
	dpkg-deb --build ~/Python/p2p/deb/relay
