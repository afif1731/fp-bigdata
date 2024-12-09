import os
from pyspark.sql import SparkSession
from datetime import date

today = date.today().strftime("%b-%d-%Y")

AWS_ACCESS_KEY = os.getenv("AWS_ACCESS_KEY")
AWS_SECRET_KEY = os.getenv("AWS_SECRET_KEY")
AWS_S3_ENDPOINT = os.getenv("AWS_S3_ENDPOINT")
AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
HIVE_METASTORE_URI = os.getenv("HIVE_METASTORE_URI")

spark = SparkSession.builder \
    .appName('Clean data') \
    .config("hive.metastore.uris", "thrift://hive-metastore:9083")\
    .config("spark.sql.warehouse.dir","s3a://datalake/warehouse")\
    .config("spark.hadoop.fs.s3a.access.key", AWS_ACCESS_KEY) \
    .config("spark.hadoop.fs.s3a.secret.key", AWS_SECRET_KEY) \
    .config("fs.s3a.endpoint", AWS_S3_ENDPOINT)\
    .config("spark.hadoop.fs.s3a.path.style.access", "true")\
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("fs.s3a.connection.ssl.enabled", "false")\
    .config('spark.hadoop.fs.s3a.aws.credentials.provider', 'org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider')\
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog")\
    .config('spark.jars','/opt/spark/jars/aws-java-sdk-bundle-1.11.375.jar')\
    .config('spark.jars','/opt/spark/jars/hadoop-aws-3.2.0.jar')\
    .config('spark.jars','/opt/spark/jars/delta-core_2.12-1.2.1.jar')\
    .enableHiveSupport()\
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

spark.sql("CREATE DATABASE IF NOT EXISTS dwh COMMENT 'Data Warehouse for Hospital'")


# Reading tables from landing area
print('\nReading ...')
patient_readmissions = spark.read.format("delta").load(f's3a://datalake/bronze/hospitaldb/{today}/patient_readmissions')

print('End of reading... \n')



# transforming tables to a set of dimensionel tables
print('\ntransforming ...')
patient_readmissions.write.format('delta').mode('overwrite').option('path','s3a://datalake/silver/warehouse/hospitaldb/Dim_patient_readmissions').saveAsTable("dwh.DimPatientReadmissions")

print('End Of Transforming')