# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "0886c934-125c-44a2-bae8-08793dfcdf6e",
# META       "default_lakehouse_name": "Gold_LakeHouse",
# META       "default_lakehouse_workspace_id": "d83c184e-82f0-4705-952c-0e29c5cb5274",
# META       "known_lakehouses": [
# META         {
# META           "id": "e003063b-04a8-42a0-8e85-b0243d356adb"
# META         },
# META         {
# META           "id": "0886c934-125c-44a2-bae8-08793dfcdf6e"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

from pyspark.sql import functions as F

df_countries_silver = spark.read.table("silver_lakehouse.dbo.Countries_Social_Barriers")


df_countries_silver.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("gold_lakehouse.dbo.Fact_Social_Barriers")

print("✅ Tabela Gold criada !")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql import functions as F

# 1. Definição do Dicionário de Mapeamento
data = [
    ("AFE", "Africa Eastern and Southern"), ("AFW", "Africa Western and Central"),
    ("ARB", "Arab World"), ("CEB", "Central Europe and the Baltics"),
    ("CHI", "Channel Islands"), ("CSS", "Caribbean small states"),
    ("EAP", "East Asia & Pacific (excluding high income)"), ("EAR", "Early-demographic dividend"),
    ("EAS", "East Asia & Pacific"), ("ECA", "Europe & Central Asia (excluding high income)"),
    ("ECS", "Europe & Central Asia"), ("EMU", "Euro area"),
    ("EUU", "European Union"), ("FCS", "Fragile and conflict affected situations"),
    ("HIC", "High income"), ("HPC", "Heavily indebted poor countries (HIPC)"),
    ("IBD", "IBRD only"), ("IBT", "IBRD & IDA total"),
    ("IDA", "IDA total"), ("IDB", "IDA blend"),
    ("IDX", "IDA only"), ("LAC", "Latin America & Caribbean (excluding high income)"),
    ("LCN", "Latin America & Caribbean"), ("LDC", "Least developed countries: UN classification"),
    ("LIC", "Low income"), ("LMC", "Lower middle income"),
    ("LMY", "Low & middle income"), ("LTE", "Late-demographic dividend"),
    ("MEA", "Middle East & North Africa (excluding high income)"), ("MIC", "Middle income"),
    ("MNA", "Middle East & North Africa"), ("NAC", "North America"),
    ("OED", "OECD members"), ("OSS", "Other small states"),
    ("PRE", "Pre-demographic dividend"), ("PSS", "Pacific island small states"),
    ("PST", "Post-demographic dividend"), ("SAS", "South Asia"),
    ("SSA", "Sub-Saharan Africa (excluding high income)"), ("SSF", "Sub-Saharan Africa"),
    ("SST", "Small states"), ("TEA", "East Asia & Pacific (IDA & IBRD countries)"),
    ("TEC", "Europe & Central Asia (IDA & IBRD countries)"), ("TLA", "Latin America & the Caribbean (IDA & IBRD countries)"),
    ("TMN", "Middle East & North Africa (IDA & IBRD countries)"), ("TSA", "South Asia (IDA & IBRD countries)"),
    ("TSS", "Sub-Saharan Africa (IDA & IBRD countries)"), ("UMC", "Upper middle income"),
    ("WLD", "World")
]

df_descricoes = spark.createDataFrame(data, ["Aggregate_Code", "Description"])

df_aggregates_silver = spark.read.table("silver_lakehouse.dbo.Global_Social_Barriers") \
    .withColumnRenamed("Country_Code_Iso3", "Aggregate_Code")

df_gold_aggregates = df_aggregates_silver.join(df_descricoes, on="Aggregate_Code", how="inner") \
    .withColumn("Entity_Type", F.lit("Aggregate/Benchmark"))

df_gold_aggregates.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("gold_lakehouse.dbo.Fact_Benchmarks")

print("✅ Tabela Gold de Agregados criada e mapeada!")
df_gold_aggregates.select("Aggregate_Code", "Description").distinct().show(5, truncate=False)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql import functions as F

df_geo_silver = spark.read.table("silver_lakehouse.dbo.geography")

df_geo_silver.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("gold_lakehouse.dbo.Dim_Geography")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql import functions as F

df_geo_silver = spark.read.table("silver_lakehouse.dbo.Dim_Date")

df_geo_silver.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("gold_lakehouse.dbo.Dim_Date")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql import functions as F

# 1. Arredondar Fact_Social_Barriers (Estrutura WIDE)
# Temos de aplicar o arredondamento a cada coluna de métrica individualmente
df_social = spark.read.table("gold_lakehouse.dbo.Fact_Social_Barriers")

metric_columns = [
    "Female_Account_Ownership", "Internet_Access", "Literacy_Rate", 
    "School_Attendance", "Child_Mortality_Rate", "Life_Expectancy", "MPI"
]

for col_name in metric_columns:
    if col_name in df_social.columns:
        df_social = df_social.withColumn(col_name, F.round(F.col(col_name), 2))

df_social.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("gold_lakehouse.dbo.Fact_Social_Barriers")
print("✅ Fact_Social_Barriers: Números arredondados.")


# 2. Arredondar Fact_Benchmarks (Estrutura LONG)
# Aqui é mais fácil, pois só existe uma coluna de valores: "Value"
df_bench = spark.read.table("gold_lakehouse.dbo.Fact_Benchmarks")

if "Value" in df_bench.columns:
    df_bench = df_bench.withColumn("Value", F.round(F.col("Value"), 2))

df_bench.write.format("delta").mode("overwrite").option("overwriteSchema", "true").saveAsTable("gold_lakehouse.dbo.Fact_Benchmarks")
print("✅ Fact_Benchmarks: Números arredondados.")

# Limpar cache para garantir que o Power BI vê os novos valores
spark.catalog.clearCache()

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql import functions as F

# 1. Carregar as fontes da Silver (Normalizando o nome para country_code_iso3 em todas)
df_gini = spark.read.table("silver_lakehouse.dbo.gini_index").select(
    F.col("Country_Code_Iso3").alias("country_code_iso3"), 
    "Year", 
    F.col("Value").alias("Gini_Index")
)

df_hdi = spark.read.table("silver_lakehouse.dbo.hdi").select(
    F.col("Country_Code_Iso3").alias("country_code_iso3"), 
    "Year", 
    F.col("Human_Development_Index").alias("HDI")
)

df_econ = spark.read.table("silver_lakehouse.dbo.economic_indicators").select(
    F.col("Country_Code_Iso3").alias("country_code_iso3"), 
    "Year", 
    "GDP_per_Capita", 
    "GDP_Annual_Growth_Pct", 
    "Inflation_CPI_Pct"
)

# 2. Unir as tabelas usando o nome comum
# Agora todas têm "country_code_iso3", por isso o join funciona perfeitamente
df_main = df_econ.join(df_gini, ["country_code_iso3", "Year"], "outer") \
                 .join(df_hdi, ["country_code_iso3", "Year"], "outer")

# 3. Arredondar e selecionar
df_final = df_main.select(
    "country_code_iso3",
    "Year",
    F.round("Gini_Index", 2).alias("Gini_Index"),
    F.round("GDP_per_Capita", 2).alias("GDP_per_Capita"),
    F.round("GDP_Annual_Growth_Pct", 2).alias("GDP_Annual_Growth_Pct"),
    F.round("Inflation_CPI_Pct", 2).alias("Inflation_CPI_Pct"),
    F.round("HDI", 3).alias("HDI")
)

# 4. Gravar na Gold
df_final.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("gold_lakehouse.dbo.Fact_Macro_Indicators")

print("✅ Fact_Macro_Indicators criada com sucesso!")
df_final.show(5)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql import functions as F

# 1. Carregar a tabela Income_Share da Silver
df_wealth = spark.read.table("silver_lakehouse.dbo.income_share")

# 2. Identificar as colunas de métricas (Percentis de rendimento)
# Geralmente são: Income_Share_Lowest_20pct, Highest_20pct, etc.
# Vamos arredondar todas as colunas exceto as de identificação
exclude_cols = ["Country_Code_Iso3", "Year"]
metric_cols = [c for c in df_wealth.columns if c not in exclude_cols]

# 3. Criar a tabela final com arredondamento e renomear colunas
df_wealth_final = df_wealth.select(
    F.col("Country_Code_Iso3"),
    F.col("Year").cast("long"),
    *[F.round(F.col(c).cast("double"), 2).alias(c) for c in metric_cols]
)

# 4. Gravar na Gold como Fact_Wealth_Distribution
df_wealth_final.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("gold_lakehouse.dbo.Fact_Wealth_Distribution")

print("✅ Fact_Wealth_Distribution criada com sucesso na Gold!")
df_wealth_final.show(5)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql import functions as F

# 1. Carregar o que já existe na Benchmarks e o que queremos adicionar (Macro Agregados)
df_bench_existente = spark.read.table("gold_lakehouse.dbo.Fact_Benchmarks")
df_macro = spark.read.table("gold_lakehouse.dbo.Fact_Macro_Indicators")
df_geo = spark.read.table("gold_lakehouse.dbo.Dim_Geography")

# 2. Isolar apenas os 51 agregados da Macro
valid_codes = df_geo.select("country_code_iso3").distinct()
df_macro_aggr = df_macro.join(valid_codes, ["country_code_iso3"], "left_anti") \
    .withColumnRenamed("country_code_iso3", "Aggregate_Code")

# 3. Fazer o MERGE (Outer Join)
# Isto vai juntar as colunas que já existiam com as novas colunas da Macro
# Se o Aggregate_Code e o Year coincidirem, ele junta na mesma linha.
df_bench_final = df_bench_existente.join(df_macro_aggr, ["Aggregate_Code", "Year"], "outer")

# 4. Limpeza: Remover a última coluna a mais (como pediste)
cols = df_bench_final.columns
df_bench_final = df_bench_final.drop(cols[-1])

# 5. Guardar com as novas colunas
df_bench_final.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("gold_lakehouse.dbo.Fact_Benchmarks")

print("✅ Fact_Benchmarks atualizada!")
print(f"Novas colunas adicionadas: {[c for c in df_macro_aggr.columns if c not in ['Aggregate_Code', 'Year']]}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql import functions as F

df_benchmarks = spark.read.table("gold_lakehouse.dbo.Fact_Benchmarks")

# Remover o Kosovo e as colunas indesejadas
df_benchmarks_clean = df_benchmarks.filter(
    F.col("Aggregate_Code") != "XKX"
).drop("Gini_Index", "MPI")

df_benchmarks_clean.write.format("delta") \
    .mode("overwrite") \
    .option("overwriteSchema", "true") \
    .saveAsTable("gold_lakehouse.dbo.Fact_Benchmarks")

print("✅ Fact_Benchmarks limpa!")
print(f"Colunas restantes: {df_benchmarks_clean.columns}")

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
