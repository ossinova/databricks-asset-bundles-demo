# Databricks Assets Bundles
[Official documentation](https://docs.databricks.com/en/dev-tools/bundles/index.html)

**TOC**
- [Introduction](#introduction)
- [Getting Started](#getting-started)
 
# Introduction 
This Repo contains an example of a Databricks Asset Bundle and Azure DevOps pipelines to deploy the bundle to stg and prod environments. The bundle covers a simple pipeline that ingests and processes sales data over bronze/silver/gold layers, unit tests and a integration test using DLT pipeline functionality.

# Getting Started
To deploy this bundle into a dev environment, you need to have Visual Studio installed. After updating the Workspace host addresses in the bundle.yml file to your Databricks Workspaces you can deploy using the 'databricks bundle deploy' command in a Bash terminal (requires latest version of Databricks CLI to be installed + authentication using 'databricks configure' or a Databricks configuration profile, see: https://docs.databricks.com/en/dev-tools/cli/authentication.html#basic-authentication). 

The ado folder also contains 2 Azure DevOps Pipeline configurations in .yaml format for deployment to staging/production environments, you can use these to create the Azure Pipelines in Azure DevOps. 

To run the Build Pipelines in Azure DevOps, following requirements are necessary:

- Import the Repo into Azure DevOps Repos
- Add this Repo (Databricks Workspace > Repos > Add > Repo) to your dev Databricks Workspace.
- Update the Workspace host addresses in the bundle.yaml file to reflect your dev/stg/prod Workspaces respectively
- Add the sales.csv files under 10_ingestion>data>dev/prod/test to the DBFS in your dev/prod/test Databricks Workspace under a dev/prod/test folder. The reason for this is that the ingestion Notebook called in dev will source from "dbfs:/FileStore/dev/sales.csv", the Notebook for stg will source from "dbfs:/FileStore/stg/sales.csv" and the Notebook for prod will source from "dbfs:/FileStore/prod/sales.csv". To simulate different data ingestion sources in the environments.
- Create a Variable Group under Pipelines>Libary called 'Bundle Deployment Variables' that has the following variables:
  - cluster-id-dev: Cluster ID of the cluster you want to run the unit tests on, for example 0821-095554-93po8zzz
  - host-dev: Host address of your dev Databricks Workspace, for example https://adb-6098755220893XXX.9.azuredatabricks.net/
  - repo-directory: Path where you have added the Repo in your dev Workspace, for example '/Repos/Repos/DatabricksDreamTeamBundle'
  - token-dev: Personal Access Token for your dev Databricks Workspace, for example dapib8af953131c9992cb7270565xxxxxxx-2
  - token-prod: Personal Access Token for your prod Databricks Workspace
  - token-stg: Personal Access Token for your stg Databricks Workspace

The Repo also contains .yaml configurations for 2 Azure DevOps pipelines explained below. These can be created in ADO under Pipelines>Pipelines>New Pipeline>Azure Repos Git. Here you can select the Azure Repo repository to which you imported this Repo. Next click 'Existing Azure Pipelines YAML file' to select the correct path for the .yaml configuration of the pipeline you want to created.

The *unittest_and_staging_deploy.yaml* defines a Azure DevOps pipeline that first runs the unit tests contained in the 50_tests>20_unit-notebooks and store the results under Test Plans>Runs in Azure DevOps. After these execute succesfully, it will deploy the bundle to your staging environment and run the sales_job. The deployment to the stg environment will also add an additional Notebook to the DLT pipeline which is under 50_tests>10_integration, this Notebook contains tests that evaluate the gold tables created by the DLT Pipeline.
This pipeline does not have a trigger, but should be added in the branch policies of your main branch under Build Validation. This will make sure that no Pull Request are able to be completed to the main branch without this pipeline succeeding. 

The *prod_deploy.yaml* defines a Azure DevOps pipeline deploys the bundle to your prod environment. 
This pipeline is set to be triggered whenever an update (merge/commit/...) is done to the main branch of your repo, so it will be triggered once any pull request to the main branch is completed.

Both pipelines can also be triggered manually by click 'Run' in Azure DevOps.

