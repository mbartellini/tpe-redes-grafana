FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app

ENV FLASK_APP=app/main.py

#TODO CHANGE THIS TO PRODUCTION WHEN READY
ENV FLASK_ENV=development

EXPOSE 3000

#IMPORTANT: 0.0.0.0 allows the app to be accessible from outside the container
CMD ["flask", "run","--host=0.0.0.0", "--port=3000"]
