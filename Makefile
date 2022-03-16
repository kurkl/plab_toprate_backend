test:
	pytest tests/

refactor:
	poetry run black ./
	poetry run isort ./

lint:
	poetry run black --check ./
	poetry run isort --recursive --check-only ./