# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "83e7b47e-7c74-45e9-a96b-b66ae0bf51aa",
# META       "default_lakehouse_name": "Bronze_LakeHouse",
# META       "default_lakehouse_workspace_id": "32338175-e0e6-4c7a-b3cf-225d1b46c410",
# META       "known_lakehouses": [
# META         {
# META           "id": "83e7b47e-7c74-45e9-a96b-b66ae0bf51aa"
# META         }
# META       ]
# META     }
# META   }
# META }

# MARKDOWN ********************

# # (1) Create Delta Tables for the UN Census Data for the Bronze Layer

# MARKDOWN ********************

# ## (1.1) Educational Data

# CELL ********************

## -------------------------------------------------------------------------------------
## Population 15 years of age and over, by educational attainment, age and sex
## -------------------------------------------------------------------------------------

import pandas as pd # Just in case for reference, but we use Spark functions here
from pyspark.sql.functions import col

# Define the folder path
folder_path = "Files/Education Statistics Database/Population 15 years of age and over, by educational attainment, age and sex/*.csv"

# Load your data
df_merged = spark.read.format("csv").option("header", "true").option("inferSchema", "true").load(folder_path)

# Automatically replace spaces and invalid characters in ALL column names
new_columns = [col(c).alias(c.replace(' ', '_').replace(',', '').replace('(', '').replace(')', '')) for c in df_merged.columns]
df_clean = df_merged.select(*new_columns)

schema = "un_census"
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {schema}")

# 3. Save to a Delta Table
target_table_name = "attainment_15plus"
df_clean.write.format("delta").mode("overwrite").saveAsTable(f"{schema}.{target_table_name}")

print(f"Merge complete! All files combined into table: {target_table_name}")



# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# ## (1.3) Economic data

# CELL ********************

## -------------------------------------------------------------------------------------
## (1) Employed population by status in employment, age and sex.csv
## (2) Gini index
## (3) Unemployment rate
## (4) Monthly employee earnings
## -------------------------------------------------------------------------------------
import pandas as pd # Just in case for reference, but we use Spark functions here
from pyspark.sql.functions import col
import os
import re

# 1. Define the directory path
input_path = "Files/Economic Statistics Database"
schema = "un_census"

# 2. List files using mssparkutils
# This returns a list of objects with .path and .name attributes
files = mssparkutils.fs.ls(input_path)

for file in files:
    if file.name.endswith(".csv"):
        base_name = file.name.rsplit('.', 1)[0]
        clean_name = re.sub(r'[^a-zA-Z0-9]', '_', base_name)
        table_name = re.sub(r'_+', '_', clean_name).lower().strip('_')
        
        print(f"Processing: {file.name} -> Table: {table_name}")
        
        df = (spark.read
              .option("header", "true")
              .option("inferSchema", "true")
              .csv(file.path))
        
        # --- NEW: CLEAN COLUMN NAMES ---
        # This replaces spaces, dots, and other bad characters in column headers
        for col_name in df.columns:
            clean_col = re.sub(r'[ ,;{}()\n\t=]', '_', col_name)
            df = df.withColumnRenamed(col_name, clean_col)
        # -------------------------------
        
        df.write.format("delta").mode("overwrite").saveAsTable(f"{schema}.{table_name}")

print("Success! All CSVs are now Delta tables with clean columns.")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# MARKDOWN ********************

# # (2) Create Delta Tables for the Data from other sources for the Bronze Layer

# MARKDOWN ********************

# ## (2.1) Wealth Inequality

# CELL ********************

## -------------------------------------------------------------------------------------
## (1) human development index
## (2) income share distribution (bottom 50%)
## (3) income share top 1%
## (4) income share top 10%
## (5) multidimensional poverty index
## -------------------------------------------------------------------------------------
import pandas as pd # Just in case for reference, but we use Spark functions here
from pyspark.sql.functions import col
import os
import re

# 1. Define the directory path
input_path = "Files/Development Statistics Database/Wealth Inequality/"
schema = "other"
spark.sql(f"CREATE SCHEMA IF NOT EXISTS {schema}")

# 2. List files using mssparkutils
# This returns a list of objects with .path and .name attributes
files = mssparkutils.fs.ls(input_path)

for file in files:
    if file.name.endswith(".csv"):
        base_name = file.name.rsplit('.', 1)[0]
        clean_name = re.sub(r'[^a-zA-Z0-9]', '_', base_name)
        table_name = re.sub(r'_+', '_', clean_name).lower().strip('_')
        
        print(f"Processing: {file.name} -> Table: {table_name}")
        
        df = (spark.read
              .option("header", "true")
              .option("inferSchema", "true")
              .csv(file.path))
        
        # --- NEW: CLEAN COLUMN NAMES ---
        # This replaces spaces, dots, and other bad characters in column headers
        for col_name in df.columns:
            clean_col = re.sub(r'[ ,;{}()\n\t=]', '_', col_name)
            df = df.withColumnRenamed(col_name, clean_col)
        # -------------------------------
        
        df.write.format("delta").mode("overwrite").saveAsTable(f"{schema}.{table_name}")

print("Success! All CSVs are now Delta tables with clean columns.")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
