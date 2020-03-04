.PHONY: release
.PHONY: install
release: 
	pyinstaller --onefile --path ~/Python/p2p/env --name Transceiver one.py 
install: 
	cp dist/Transceiver-dev /usr/bin/transciver
