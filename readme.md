# PyFS
File Server python

## Principais frameworks utilizados
- [Flask](https://github.com/pallets/flask) - WSGI Web
- [SQLAlchemy](https://www.sqlalchemy.org/) - ORM Database
- [Swagger](https://swagger.io/tools/swagger-ui/) Documentação e Teste de API’s 

### Swagger UI Operations
![Swagger UI](https://raw.githubusercontent.com/rogeriorocha/pyfs/master/docs/swagger-ui.png)

## Run local
```bash
git clone git@github.com:rogeriorocha/pyFS.git
cd pyFS
# install dependencias
pip install -r requirements.txt
python wsgi.py
```

## Run in docker
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

## Comandos uteis Docker
* Lista conteiners
```bash
docker ps
```
Vai aparecer uma tabela com

**CONTAINER ID** - ID do container<br>
**IMAGE** - a imagem que foi utilizada para gerar esse container<br>
**COMMAND** - o comando passado como parâmetro para esse container (exemplo o /bin/bash)<br>
**CREATED** - a data da criação do container<br>
**STATUS** - o estado do container (parado ou em funcionamento)<br>
**PORTS** - as portas compartilhadas entre host e container<br>
**NAMES** - e o nome que você deu ao container, se o fez<br>
O ps só vai mostrar os containers que estão em atividade, para verificar todos os containers criados, incluindo os que estiverem parados, utilize o ps -a:


* Entrar no countainer
```bash
docker exec -it <CONTAINER_ID> /bin/bash
```

* Limpar todos conteiners/volumes
```bash
docker stop $(docker ps -a -q); docker rm $(docker ps -a -q); docker volume rm $(docker volume ls -qf dangling=true)
```

* Listar imagens
```bash
docker image ls
```

* Criar um container e entrar no Terminal
```bash
docker run -it ubuntu /bin/bash
# -i significa interatividade 
# -t significa que queremos um link com o Terminal do container.
```

* Informações de uso de Hardware do container:
```bash
docker stats <id_ou_apelido>
```

Veremos informações como:

**CONTAINER** - ID do Container<br>
**CPU %** - uso de CPU em porcentagem<br>
**MEM USAGE / LIMIT** - Memória usada/Limite que você pode ter setado<br>
**MEM** - uso de memória em porcentagem<br>
**NET I/O** - I/O de Internet<br>
**BLOCK IO** - Outros processos de I/O.<br>

* Criar nova imagem
Ele vai gerar uma nova imagem a partir desse commit.
```bash
docker commit <ID/apelido> <nome_da_nova_imagem>
```

* Mapeando uma porta para o container
Usamos o comando -p <PORT_HOST>:<PORT_CONTAINER>

```bash
docker run -it -p 8080:80 ubuntu
```

* Montar containers auto destrutivos
Usando o comando --rm, podemos montar containers que se destroem ao sairmos da sessão.
```bash
docker run -it --rm -p 8080:80 nginx /bin/bash
```


* Executando containers em segundo plano
Podemos executar o container e deixar ele em segundo plano, sem precisar ficar conectado pelo Shell, com o comando -d.

```bash
docker run -d -p 8080:80 nginx /usr/sbin/nginx -g
```

* Para controlar esse container usamos os comandos stop e start:
```bash
docker stop <id_ou_apelido>
docker start <id_ou_apelido>
```


### others
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


### kubernets
```bash
docker build -t rogeriosilvarocha/pyfs:latest . --no-cache



#auto scale
kubectl run py-fs --image=rogeriosilvarocha/pyfs:latest --image-pull-policy=Never --requests=cpu=200m --limits=cpu=500m --expose --port=5000
kubectl autoscale deployment py-fs --cpu-percent=50 --min=1 --max=10


curl 10.110.216.231:5000/FS/cpu-inc/

kubectl get deployment py-fs
kubectl get hpa

#stress
kubectl run -i --tty load-generator --image=busybox /bin/sh
> while true; do wget -q -O- http://10.110.216.231:5000/FS/cpu-inc/; done
> while true; do wget -q -O- http://py-fs.default.svc.cluster.local:5000/FS/cpu-inc/; done

kubectl delete hpa py-fs
kubectl delete svc py-fs
kubectl delete deployment py-fs
kubectl delete deployment load-generator







kubectl expose rc example --port=8765 --target-port=9376 --name=example-service --type=LoadBalancer


docker build -t rogeriosilvarocha/pyfs:latest . --no-cache



# auto scale
kubectl run py-fs --image=rogeriosilvarocha/pyfs:latest --image-pull-policy=Never --requests=cpu=200m --limits=cpu=500m --expose --port=5000
kubectl autoscale deployment py-fs --cpu-percent=50 --min=1 --max=10


curl 10.110.216.231:5000/FS/cpu-inc/

kubectl get deployment py-fs
kubectl get hpa

#stress
kubectl run -i --tty load-generator --image=busybox /bin/sh
> while true; do wget -q -O- http://10.110.216.231:5000/FS/cpu-inc/; done
> while true; do wget -q -O- http://py-fs.default.svc.cluster.local:5000/FS/cpu-inc/; done

kubectl delete hpa py-fs
kubectl delete svc py-fs
kubectl delete deployment py-fs
kubectl delete deployment load-generator




-- test
```

