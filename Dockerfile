FROM python:3.13-slim

WORKDIR /app

RUN pip install uv

COPY . .

EXPOSE 8000

CMD ["uv", "run", "manage.py", "runserver", "0.0.0.0:8000"]
