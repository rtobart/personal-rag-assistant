FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .

RUN pip3 install

COPY . .

EXPOSE 3001

CMD ["python3", "run.py"]