install:
	pip install -r requirements.txt

run:
	python -m mini_budget_tracker.budget_tracker

test:
	pytest tests
