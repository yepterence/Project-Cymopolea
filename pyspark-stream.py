#!/usr/bin/env python

import pyspark
from pyspark.sql import SparkSession
from pyspark.sql.types import StringType, StructType, StructField

spark_ver = pyspark.__version__
KAFKA_TOPIC = "natural_disasters"
KAFKA_SERVER = "localhost:9092"
# Instantiate spark object creator
builder = SparkSession \
    .builder \
    .appName("NaturalDisasters") \
    .getOrCreate()
# schema for incoming tweets
data_schema = StructType([StructField("tweet_id", StringType()),
                          StructField("tweet_text", StringType()),
                          StructField("created_at", StringType()),
                          StructField("author_id", StringType())])
# if using pyspark, data will need to be converted to list of tuples
# converted_data = list(data.items())

# subscribe to kafka and store data in dataframe format
df = builder \
    .readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", KAFKA_SERVER) \
    .option("subscribe", KAFKA_TOPIC) \
    .option("startingOffsets", "earliest") \
    .load()

print(df.selectExpr("CAST(value AS STRING)"))

# df.show(False)
