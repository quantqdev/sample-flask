start-dev:
	flask --app src/hello run

start-debug:
	flask --app src/hello run --debug

start-prod:
	gunicorn -w 4 -b 0.0.0.0 'src.hello:app'

clean:
	rm -rf __pycache__/ .venv/