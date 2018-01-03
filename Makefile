.PHONY: pip, fetch, clean

pip:
	pip install -r requirements.txt

fetch:
	@echo "Current datetime: $(shell date)"
	python daily_deal.py

clean:
	@echo "make clean ..."
	@find ./ -name '*.pyc' -exec rm -f {} +
	@find ./ -name '*.pyo' -exec rm -f {} +
	@find ./ -name '*~' -exec rm -f {} +
	@find ./ -name '__pycache__' -exec rm -rf {} +
