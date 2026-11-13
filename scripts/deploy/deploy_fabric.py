
import os
from pathlib import Path

from azure.identity import ClientSecretCredential
from fabric_cicd import FabricWorkspace, publish_all_items

# Repository root
ROOT_DIR = Path(__file__).resolve().parents[2]
FABRIC_DIR = ROOT_DIR

# Read environment variables
tenant_id = os.environ["AZURE_TENANT_ID"]
client_id = os.environ["AZURE_CLIENT_ID"]
client_secret = os.environ["AZURE_CLIENT_SECRET"]
workspace_id = os.environ["FABRIC_WORKSPACE_ID"]

# Authenticate using Service Principal
credential = ClientSecretCredential(
    tenant_id=tenant_id,
    client_id=client_id,
    client_secret=client_secret,
)

# Configure target Fabric workspace
target_workspace = FabricWorkspace(
    workspace_id=workspace_id,
    repository_directory=str(FABRIC_DIR),
    item_type_in_scope=[
        "Lakehouse",
        "Notebook",
        "DataPipeline",
        "Report",
        "SemanticModel",
    ],
    token_credential=credential,
)

print(f"Starting deployment to workspace: {workspace_id}...")
publish_all_items(target_workspace)
print("Deployment completed successfully.")
