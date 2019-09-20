# Dockerfile - this is a comment. Delete me if you want.
#FROM python:3.7
FROM python:3.7.4-alpine
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["wsgi.py"]
