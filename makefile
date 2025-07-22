run:
	poetry run streamlit run app.py --server.port 8080

ruff-check:
	poetry run ruff check .
	poetry run ruff format . --check

ruff-fix:
	poetry run ruff check . --fix
	poetry run ruff format .
