FROM python:3.10.6-alpine

# We copy just the requirements.txt first to leverage Docker cache
COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install -r requirements.txt

ENV FLASK_RUN_HOST=0.0.0.0

COPY . /app

EXPOSE 5000

CMD ["flask", "run"]