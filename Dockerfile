FROM python:3
COPY . /user/scr/app
WORKDIR /user/scr/app
RUN pip install -r requirements.txt
CMD [ "python3", "manage.py", "runserver", "0.0.0.0:8000"]