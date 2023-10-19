FROM python:3.12

RUN mkdir /server
WORKDIR /server
COPY ./estate_db ./estate_db
RUN pip install ./estate_db
COPY ./server/requirements.txt .
RUN pip install -r requirements.txt
COPY ./server .
CMD ["gunicorn", "server:create_app()", "--bind", "0.0.0.0:8080"]