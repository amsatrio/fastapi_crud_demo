lib:
	pip install -r requirement.txt

dev:
	fastapi dev ./src --port 8989 --host 0.0.0.0
prod:
	fastapi run ./src --port 8989 --host 0.0.0.0