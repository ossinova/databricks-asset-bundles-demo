# Databricks notebook source
#import os 

schema = "name string, brand string, quantity int"
#df = spark.read.schema(schema).options(header=True).csv(f"file:{os.getcwd()}/data/dev/sales.csv")
df = spark.read.schema(schema).options(header=True).csv(f"dbfs:/FileStore/prod/sales.csv")
df.write.mode("overwrite").saveAsTable("sales")
