FROM python:3.11-slim-bullseye
WORKDIR /app
COPY ./requirements.txt requirements.txt
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "main:app","--workers", "5", "--host", "0.0.0.0", "--port", "8000"]
