.PHONY: release

all: one.py

one.py:
	pyinstaller --onefile --path ~/Python/p2p/env --name SFT-dev one.py
release: 
	pyinstaller --onefile --path ~/Python/p2p/env --name SFT one.py
