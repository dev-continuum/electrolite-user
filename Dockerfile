#
FROM python:3.9

#
WORKDIR /code

#
COPY ./requirements.txt /code/requirements.txt


#
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

#
COPY ./app /code/app
COPY ./data_store /code/data_store
COPY ./utility /code/utility
COPY config/dev.env /code/.env
COPY ./config.py /code/config.py
COPY ./main.py /code/main.py
#

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "9000"]
