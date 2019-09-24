# PyFS
File Server python

##


## Run em docker
Clone this repository on your Docker host and...:
```bash
git clone git@github.com:rogeriorocha/pyFS.git
cd pyFS
#build image
docker build -t rogeriosilvarocha/pyfs:latest . 
#run conteiner
docker run -p 5000:5000 -e SQLALCHEMY_DATABASE_URI='sqlite:///:memory:' rogeriosilvarocha/pyfs:latest

#run conteiner salvando os dados no host
docker run -p 5000:5000 -e SQLALCHEMY_DATABASE_URI='sqlite:////dados/store/site.db' -v /tmp/store:/dados/store rogeriosilvarocha/pyfs:latest
```

```code
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org PyPDF2

pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org pyPdf

pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org reportlab
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org flask_swagger_ui
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org pymssql
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org timeloop --user
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org reportlab --user
pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org zlib --user

pip freeze > requirements.txt
pip install -r requirements.txt
```
