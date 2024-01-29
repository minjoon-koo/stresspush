FROM python:3.8.9
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
RUN pip install gunicorn
EXPOSE 80
CMD ["gunicorn", "api.wsgi:application", "--bind", "0.0.0.0:80"]
#CMD ["python","/app/manage.py","runserver","--bind","0.0.0.0:80"]
