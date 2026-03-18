.PHONY: setup run test-osc test-channels ui clean help

ifeq ($(OS),Windows_NT)
    PYTHON = venv\Scripts\python.exe
    PIP = venv\Scripts\pip.exe
else
    PYTHON = ./venv/bin/python
    PIP = ./venv/bin/pip
endif

setup:
	python -m venv venv
	"$(PYTHON)" -m pip install --upgrade pip
	"$(PIP)" install -r requirements.txt

run:
	"$(PYTHON)" main/main.py

ui:
	@echo "Starting web UI server..."
	@echo "Open http://localhost:5000 in your browser"
	"$(PYTHON)" UI/server.py

test-osc:
	"$(PYTHON)" main/test_osc.py

test-channels:
	"$(PYTHON)" main/test_channels.py

clean:
	python -c "import shutil, pathlib; shutil.rmtree('venv', ignore_errors=True); shutil.rmtree('UI/uploads', ignore_errors=True); [shutil.rmtree(p, ignore_errors=True) for p in pathlib.Path('.').rglob('__pycache__')]; [p.unlink() for p in pathlib.Path('.').rglob('*.pyc') if p.exists()]"

help:
	@echo "Available commands:"
	@echo "  make setup          - Create venv and install dependencies"
	@echo "  make run            - Run the main program"
	@echo "  make ui             - Run the web UI server"
	@echo "  make test-osc       - Test OSC connection"
	@echo "  make test-channels  - Test DMX channels"
	@echo "  make clean          - Remove venv and cache files"
	@echo "  make help           - Show this help message"