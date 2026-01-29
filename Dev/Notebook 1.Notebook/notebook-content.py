# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "2040f8e7-720b-4901-acd5-9b9c700b12af",
# META       "default_lakehouse_name": "Bronze_LakeHouse",
# META       "default_lakehouse_workspace_id": "d83c184e-82f0-4705-952c-0e29c5cb5274",
# META       "known_lakehouses": [
# META         {
# META           "id": "2040f8e7-720b-4901-acd5-9b9c700b12af"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

from pyspark.sql import functions as F

unemployment_raw = (
    spark.read
    .option("header", True)
    .option("inferSchema", True)
    .csv("Files/unemployment_worldbank.csv")
)

display(unemployment_raw)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql import functions as F

def clean_columns(df):
    for col in df.columns:
        clean_col = (
            col.lower()
               .replace(" ", "_")
               .replace("-", "_")
        )
        df = df.withColumnRenamed(col, clean_col)
    return df

unemployment_clean = clean_columns(unemployment_raw)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

(
    unemployment_clean
    .write
    .format("delta")
    .mode("overwrite")
    .saveAsTable("world_bank.unemployment")
)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
