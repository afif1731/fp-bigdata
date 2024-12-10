#!/bin/sh

export HADOOP_HOME=/opt/hadoop-3.3.1
export HADOOP_CLASSPATH=${HADOOP_HOME}/share/hadoop/tools/lib/aws-java-sdk-bundle-1.11.375.jar:${HADOOP_HOME}/share/hadoop/tools/lib/hadoop-aws-3.3.1.jar
export JAVA_HOME=/usr/local/openjdk-11
export CLASSPATH=$HIVE_HOME/lib/mysql-connector-j-8.2.0.jar

# Initialize schema if not already initialized
echo "Checking Hive Metastore schema..."
/opt/apache-hive-metastore-3.0.0-bin/bin/schematool -info -dbType mysql
if [ $? -ne 0 ]; then
    echo "Initializing Hive Metastore schema..."
    /opt/apache-hive-metastore-3.0.0-bin/bin/schematool -initSchema -dbType mysql
else
    echo "Schema already initialized."
fi

# Start the Hive Metastore service
echo "Starting Hive Metastore..."
/opt/apache-hive-metastore-3.0.0-bin/bin/start-metastore
if [ $? -ne 0 ]; then
    echo "Failed to start Hive Metastore. Exiting."
    exit 1
fi
