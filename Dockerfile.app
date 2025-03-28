FROM python:3.13

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

EXPOSE 8000

# TODO: separate compose file for local dev (for hot reloading)
# --env-file .env makes uvicorn auto load env vars so that load_dotenv() is not needed
ENTRYPOINT [ "uvicorn", "app.main:app", "--env-file", ".env", "--reload", "--host", "0.0.0.0", "--port", "8000" ]