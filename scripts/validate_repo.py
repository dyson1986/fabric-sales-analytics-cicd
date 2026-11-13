
trigger:
  branches:
    include:
      - main

pool:
  vmImage: 'ubuntu-latest'

variables:
  - group: fabric-cicd-secrets
  - group: fabric-cicd-config

stages:

# STAGE 1: Validate repository
- stage: Validate
  displayName: 'Validate Fabric Repository'
  jobs:
  - job: ValidateRepo
    displayName: 'Check Fabric Items'
    steps:
    - checkout: self

    - task: UsePythonVersion@0
      inputs:
        versionSpec: '3.12'

    - script: |
        python -m pip install --upgrade pip
        python -m pip install -r "$(Build.SourcesDirectory)/requirements.txt"
        python "$(Build.SourcesDirectory)/scripts/validate_repo.py"
      displayName: 'Validate Fabric repository'

# STAGE 2: Deploy to TEST only
- stage: Deploy_Test
  displayName: 'Deploy to TEST'
  dependsOn: Validate
  condition: succeeded()
  jobs:
  - job: DeployTest
    displayName: 'Publish Fabric Items to TEST'
    steps:
    - checkout: self

    - task: UsePythonVersion@0
      inputs:
        versionSpec: '3.12'

    - script: |
        python -m pip install -r "$(Build.SourcesDirectory)/requirements.txt"
        python -u "$(Build.SourcesDirectory)/scripts/deploy/deploy_fabric.py"
      displayName: 'Deploy Fabric items to TEST'
      env:
        AZURE_TENANT_ID: $(AZURE_TENANT_ID)
        AZURE_CLIENT_ID: $(AZURE_CLIENT_ID)
        AZURE_CLIENT_SECRET: $(AZURE_CLIENT_SECRET)
        FABRIC_WORKSPACE_ID: $(FABRIC_TEST_WORKSPACE_ID)
        FABRIC_ENVIRONMENT: TEST
