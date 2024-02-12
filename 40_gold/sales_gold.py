# Databricks notebook source
#Databricks notebook source
import dlt
from pyspark.sql.functions import sum

@dlt.table(
  comment='Transforming data to silver')
def sales_gold():
    
    #Read in silver table
    gdf = dlt.read('sales_silver')
    
    #Sum QuantitySold per Brand
    gdf = gdf.groupBy("Brand").agg(sum("QuantitySold").alias("QuantitySoldPerBrand"))

    return gdf
