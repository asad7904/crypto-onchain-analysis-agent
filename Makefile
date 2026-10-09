install:
	python -m pip install -r requirements.txt

run:
	uvicorn crypto_agent.main:app --reload

up:
	docker compose up --build

down:
	docker compose down -v

test:
	pytest -q
