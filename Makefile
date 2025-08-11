.PHONY: build run test lint fmt clean

build:
	docker build -t ai-infer:dev .

run:
	docker compose up --build

test:
	PYTHONPATH=./app pytest -q app/tests

lint:
	python -m pyflakes app || true

fmt:
	python -m black app || true

clean:
	docker system prune -f || true
	rm -rf __pycache__ .pytest_cache || true
