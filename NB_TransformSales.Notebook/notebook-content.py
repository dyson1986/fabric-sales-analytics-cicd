# Fabric notebook source

# METADATA ********************

# META {
# META   "kernel_info": {
# META     "name": "synapse_pyspark"
# META   },
# META   "dependencies": {
# META     "lakehouse": {
# META       "default_lakehouse": "897d62f6-47a7-419b-8038-bdc74bcc0603",
# META       "default_lakehouse_name": "LH_SalesAnalytics",
# META       "default_lakehouse_workspace_id": "ee32ee6e-6a87-41a9-b7dd-6eba291bbfe5",
# META       "known_lakehouses": [
# META         {
# META           "id": "897d62f6-47a7-419b-8038-bdc74bcc0603"
# META         }
# META       ]
# META     }
# META   }
# META }

# CELL ********************

full_path = "abfss://Sales-Analytics1-DEV@onelake.dfs.fabric.microsoft.com/LH_SalesAnalytics.Lakehouse/Files/sales/sales.csv"

notebookutils.fs.ls(
    "abfss://Sales-Analytics1-DEV@onelake.dfs.fabric.microsoft.com/LH_SalesAnalytics.Lakehouse/Files/sales/"
)

# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************

from pyspark.sql import functions as F
 
source_path = "Files/sales/sales.csv"

df = (spark.read
      .option("header", True)
      .option("inferSchema", True)
      .csv(full_path))
 
required = ["OrderID", "OrderDate", "Region", "Country",
            "Product", "Category", "Quantity", "UnitPrice", "Discount"]
 
missing = [c for c in required if c not in df.columns]
if missing:
    raise ValueError(f"Missing required columns: {missing}")
 
clean = (df
    .dropna(subset=["OrderID", "OrderDate", "Region", "Product"])
    .dropDuplicates(["OrderID"])
    .filter((F.col("Quantity") > 0) & (F.col("UnitPrice") >= 0))
    .withColumn("OrderDate", F.to_date("OrderDate"))
    .withColumn("GrossSales", F.col("Quantity") * F.col("UnitPrice"))
    .withColumn("NetSales",
                F.col("Quantity") * F.col("UnitPrice") *
                (F.lit(1) - F.coalesce(F.col("Discount"), F.lit(0))))
)
 
clean.write.format("delta").mode("overwrite").saveAsTable("sales_silver")
 
gold = (clean
    .groupBy("Region", "Product", "Category")
    .agg(
        F.countDistinct("OrderID").alias("OrderCount"),
        F.sum("Quantity").alias("UnitsSold"),
        F.sum("GrossSales").alias("GrossSales"),
        F.sum("NetSales").alias("NetSales")
    )
)
 
gold.write.format("delta").mode("overwrite").saveAsTable("sales_gold_region_product")
 
display(gold)


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }

# CELL ********************


# METADATA ********************

# META {
# META   "language": "python",
# META   "language_group": "synapse_pyspark"
# META }
