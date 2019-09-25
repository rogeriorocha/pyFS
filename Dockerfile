# Dockerfile - this is a comment. Delete me if you want.
FROM python:3.7.4-slim
COPY . /app
WORKDIR /app
ENV SQLALCHEMY_DATABASE_URI 'sqlite:///site.db'
ENV FS_PATH_STORE '/dados/store'
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["wsgi.py"]
