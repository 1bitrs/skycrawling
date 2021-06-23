

### 安装Skywalking

```shell
docker pull elasticsearch:6.8.16
docker pull apache/skywalking-ui:8.0.1
docker pull apache/skywalking-oap-server:8.0.1-es6
```

```shell
docker run --name elasticsearch6 -p 9200:9200 -p 9300:9300 \
-e "discovery.type=single-node" \
-e ES_JAVA_OPTS="-Xms512m -Xmx1024m" \
-v ~/docker/elasticsearch6/config/elasticsearch.yml:/usr/share/elasticsearch/config/elasticsearch.yml \
-v ~/docker/elasticsearch6/data:/usr/share/elasticsearch/data \
-v ~/docker/elasticsearch/plugins:/usr/share/elasticsearch/plugins \
-d elasticsearch:6.8.16
```

```shell
docker run --name skywalking-oap-server  -d -p 1234:1234 -p 11800:11800 -p 12800:12800 --restart always --link elasticsearch6:elasticsearch6 -e SW_STORAGE=elasticsearch -e SW_STORAGE_ES_CLUSTER_NODES=elasticsearch6:9200 apache/skywalking-oap-server:8.0.1-es6
```

```shell
docker run --name skywalking-ui -d -p 8080:8080 --link skywalking-oap-server:skywalking-oap-server -e SW_OAP_ADDRESS=skywalking-oap-server:12800 apache/skywalking-ui:8.0.1
```

### 生成数据库表模型

```shell
sqlacodegen mysql+pymysql://root:root@localhost:3306/skycrawling
```