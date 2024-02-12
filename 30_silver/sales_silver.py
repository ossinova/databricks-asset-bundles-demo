# Databricks notebook source
#Databricks notebook source
import dlt

@dlt.table(
  comment='Transforming data to silver')
def sales_silver():
    
    #Read in bronze table
    sdf = dlt.read('sales_bronze')
    
    sdf = sdf.withColumnRenamed('name', 'ModelName')
    sdf = sdf.withColumnRenamed('brand', 'Brand')
    sdf = sdf.withColumnRenamed('quantity', 'QuantitySold')
    
    return sdf
