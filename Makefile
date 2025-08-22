lib:
	pip install -r requirement.txt

dev:
	fastapi dev ./src --port 8989 --host 0.0.0.0
prod:
	fastapi run ./src --port 8989 --host 0.0.0.0

activate_web_env:
	source /home/user0/miniconda3/bin/activate web 
deactivate:
	source /home/user0/miniconda3/bin/deactivate