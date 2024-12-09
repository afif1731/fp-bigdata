import os
from pyspark.sql import SparkSession
from datetime import date

# Get today's date for partitioning
today = date.today().strftime("%b-%d-%Y")

# Validate and fetch environment variables
def get_env_var(var_name):
    value = os.getenv(var_name)
    if not value:
        raise ValueError(f"Environment variable '{var_name}' is not set!")
    return value

AWS_ACCESS_KEY = get_env_var("AWS_ACCESS_KEY")
AWS_SECRET_KEY = get_env_var("AWS_SECRET_KEY")
AWS_S3_ENDPOINT = get_env_var("AWS_S3_ENDPOINT")
AWS_BUCKET_NAME = get_env_var("AWS_BUCKET_NAME")

POSTGRES_USER = get_env_var("POSTGRES_USER")
POSTGRES_PASSWORD = get_env_var("POSTGRES_PASSWORD")
POSTGRES_ENDPOINT = get_env_var("POSTGRES_ENDPOINT")
POSTGRES_DB = get_env_var("POSTGRES_DB")

# Initialize SparkSession
spark = SparkSession.builder \
    .appName('Postgres to S3 pipeline') \
    .config("spark.hadoop.fs.s3a.access.key", AWS_ACCESS_KEY) \
    .config("spark.hadoop.fs.s3a.secret.key", AWS_SECRET_KEY) \
    .config("fs.s3a.endpoint", AWS_S3_ENDPOINT) \
    .config("spark.hadoop.fs.s3a.path.style.access", "true") \
    .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem") \
    .config("fs.s3a.connection.ssl.enabled", "false") \
    .config("spark.hadoop.fs.s3a.aws.credentials.provider", "org.apache.hadoop.fs.s3a.SimpleAWSCredentialsProvider") \
    .config("spark.sql.extensions", "io.delta.sql.DeltaSparkSessionExtension") \
    .config("spark.sql.catalog.spark_catalog", "org.apache.spark.sql.delta.catalog.DeltaCatalog") \
    .config("spark.delta.logStore.class", "io.delta.storage.S3SingleDriverLogStore") \
    .config('spark.jars', 
        '/opt/spark/jars/aws-java-sdk-bundle-1.11.375.jar,'
        '/opt/spark/jars/hadoop-aws-3.2.0.jar,'
        '/opt/spark/jars/delta-core_2.12-1.2.1.jar,'
        '/opt/spark/jars/postgresql-42.3.5.jar') \
    .getOrCreate()

spark.sparkContext.setLogLevel("ERROR")

# List of tables to process
table_names = ['patient_readmissions']

# PostgreSQL connection URL
postgres_url = f"jdbc:postgresql://{POSTGRES_ENDPOINT}/{POSTGRES_DB}"

# Loop through tables
for table_name in table_names:
    print(f"Processing table: {table_name}...")
    
    # Read table from PostgreSQL
    df = spark.read \
        .format("jdbc") \
        .option("url", postgres_url) \
        .option("dbtable", table_name) \
        .option("user", POSTGRES_USER) \
        .option("password", POSTGRES_PASSWORD) \
        .option("driver", "org.postgresql.Driver") \
        .load()
    
    # Write table to Delta format in S3
    s3_path = f"s3a://{AWS_BUCKET_NAME}/bronze/hospitaldb/{today}/{table_name}"
    df.write \
        .format("delta") \
        .mode("overwrite") \
        .save(s3_path)
    
    print(f"Table {table_name} has been processed and saved to {s3_path}.")
