.PHONY: setup run test-osc test-channels clean help

# Setup virtual environment and install dependencies
setup:
	python3 -m venv venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r requirements.txt

# Run the main program
run:
	./venv/bin/python main/main.py

# Test OSC connection to QLC+
test-osc:
	./venv/bin/python main/test_osc.py

# Test DMX channels
test-channels:
	./venv/bin/python main/test_channels.py

# Clean up virtual environment and cache files
clean:
	rm -rf venv
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

# Show available commands
help:
	@echo "Available commands:"
	@echo "  make setup         - Create venv and install dependencies"
	@echo "  make run          - Run the main program"
	@echo "  make test-osc     - Test OSC connection"
	@echo "  make test-channels - Test DMX channels"
	@echo "  make clean        - Remove venv and cache files"
	@echo "  make help         - Show this help message"