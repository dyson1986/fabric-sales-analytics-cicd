from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

required_items = [
    "LH_SalesAnalytics.Lakehouse",
    "NB_TransformSales.Notebook",
    "PL_LoadSales.DataPipeline",
    "RPT_SalesOverview.Report",
    "RPT_SalesOverview.SemanticModel",
]

print("Starting Fabric repository validation...")

for item in required_items:
    item_path = ROOT_DIR / item

    if item_path.exists():
        print(f"PASS: {item}")
    else:
        raise FileNotFoundError(f"Missing required item: {item}")

print("Repository validation completed successfully.")
