# Databricks notebook source
import dlt

landingzone = 'dbfs:/user/hive/warehouse'

# Location to fetch landing data reports
path = landingzone + "/sales"

@dlt.table(
  comment='Reading data to bronze')
def sales_bronze():
    return (spark.read.load(path))
