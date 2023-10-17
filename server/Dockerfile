FROM python:3.12

RUN mkdir /server
WORKDIR /server
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["gunicorn", "server:app", "--reload", "--bind", "0.0.0.0:8080"]