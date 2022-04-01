test:
	pytest tests/

coverage-r:
	coverage report -m

refactor:
	poetry run black ./
	poetry run isort ./

lint:
	poetry run black --check ./
	poetry run isort --recursive --check-only ./

# Docker
build:
	docker build -t plab_toprate_backend/app -f Dockerfile .

dev-test:
	docker-compose -f docker-compose-dev.yml up --abort-on-container-exit