FROM openjdk:11-jre

WORKDIR /opt

ENV HADOOP_VERSION=3.3.1
ENV METASTORE_VERSION=3.1.2

ENV HADOOP_HOME=/opt/hadoop-${HADOOP_VERSION}
ENV HIVE_HOME=/opt/apache-hive-metastore-${METASTORE_VERSION}-bin

RUN curl -L https://repo1.maven.org/maven2/org/apache/hive/hive-standalone-metastore/${METASTORE_VERSION}/hive-standalone-metastore-${METASTORE_VERSION}-bin.tar.gz | tar zxf - && \
    curl -L https://archive.apache.org/dist/hadoop/common/hadoop-${HADOOP_VERSION}/hadoop-${HADOOP_VERSION}.tar.gz | tar zxf -

RUN curl -o mysql-connector-j-8.0.33.jar https://repo1.maven.org/maven2/mysql/mysql-connector-j/8.0.33/mysql-connector-j-8.0.33.jar && \
    cp mysql-connector-j-8.0.33.jar ${HIVE_HOME}/lib/ 

COPY metastore-site.xml ${HIVE_HOME}/conf
COPY entrypoint.sh /entrypoint.sh

RUN groupadd -r hive --gid=1000 && \
    useradd -r -g hive --uid=1000 -d ${HIVE_HOME} hive && \
    chown hive:hive -R ${HIVE_HOME} && \
    chown hive:hive /entrypoint.sh && chmod +x /entrypoint.sh

USER hive
EXPOSE 9083

ENTRYPOINT ["sh", "-c", "/entrypoint.sh"]