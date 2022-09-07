#!/usr/bin/env python

import pyspark
from pyspark.sql import SparkSession

spark_ver = pyspark.__version__

# Instantiate spark object creator
builder = SparkSession \
        .builder\
        .appName("NaturalDisasters")\
        .getOrCreate()

# subscribe to kafka and store data in dataframe format
df = builder \
    .readStream \
    .format("kafka")\
    .option("subscribe", "disasters")\
    .option("kafka.bootstrap.servers", "localhost:9092")\
    .load()

df.selectExpr("CAST(value AS STRING)")

df.show(False)






