# Databricks notebook source
# This notebook defines tests for DLT pipeline
# It could be defined in SQL as well (potentially i)

# COMMAND ----------

import dlt

# COMMAND ----------

@dlt.table(comment="Check number of records")
@dlt.expect_or_fail("valid count", "count = 3 or count = 0") # we need to check for 0 because DLT first evaluates with empty dataframe
def sales_gold_count_check():
  cnt = dlt.read("sales_gold").count()
  return spark.createDataFrame([[cnt]], schema="count long")

# COMMAND ----------

@dlt.table(comment="Check type")
@dlt.expect_all_or_fail({"valid Brand": "Brand in ('BMW', 'Mercedes','Audi')",
                         "Brand is not null": "Brand is not null"})
def sales_gold_brand_check():
  return dlt.read("sales_gold").select("Brand")
