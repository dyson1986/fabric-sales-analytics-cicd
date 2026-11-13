import os
from pathlib import Path

from azure.identity import ClientSecretCredential
from fabric_cicd import FabricWorkspace, publish_all_items

# Repository root is one level above the deploy folder
ROOT_DIR = Path(__file__).resolve().parent.parent
FABRIC_DIR = ROOT_DIR / "fabric"

# Read deployment settings from Azure DevOps variables
tenant_id = os.environ["AZURE_TENANT_ID"]
client_id = os.environ["AZURE_CLIENT_ID"]
client_secret = os.environ["AZURE_CLIENT_SECRET"]
workspace_id = os.environ["FABRIC_WORKSPACE_ID"]
environment = os.getenv("FABRIC_ENVIRONMENT", "TEST")

# Authenticate using the Azure service principal
credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=client_id,
    client_secret=client_secret,
)

# Deploy Lakehouse, Notebook and Data Pipeline items
target_workspace = FabricWorkspace(
    workspace_id=workspace_id,
    environment=environment,
    repository_directory=str(FABRIC_DIR),
    item_type_in_scope=["Lakehouse", "Notebook", "DataPipeline"],
    token_credential=credential,
)

print(f"Starting deployment to {environment}...")
publish_all_items(target_workspace)
print(f"Deployment to {environment} completed successfully.")
