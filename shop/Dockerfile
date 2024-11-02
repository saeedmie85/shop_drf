FROM python:3.10

WORKDIR /code

COPY requirements.txt /code/

RUN pip3 install -U pip
RUN pip3 install -r requirements.txt

COPY . /code/

EXPOSE 8000

# CMD ["python3", "manage.py", "runserver", "0.0.0.0:8000"]


