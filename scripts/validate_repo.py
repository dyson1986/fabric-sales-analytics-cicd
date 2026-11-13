from pathlib import Path

required_items = [
    "fabric/LH_SalesAnalytics.Lakehouse",
    "fabric/NB_TransformSales.Notebook",
    "fabric/PL_LoadSales.DataPipeline",
]

print("Starting Fabric repository validation...")

for item in required_items:
    if Path(item).exists():
        print(f"PASS: {item}")
    else:
        raise FileNotFoundError(f"Missing required item: {item}")

print("Repository validation completed successfully.")
