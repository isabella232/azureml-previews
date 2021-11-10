# Connect to Jupyter Notebook with "az ml notebook up" in CLI v2 (Private Preview)

## Overview 

ML professionals are used to typing `jupyter notebook` to start their ML data & training workflows.  With `az ml notebook up`, Azure ML users can now move their code & notebooks to the cloud in one CLI command, and start using cloud data and compute in their workflows. 

## Prerequisite 

* Azure subscription. If you don't have an Azure subscription, , sign up to try the [free or paid version of Azure Machine Learning](https://azure.microsoft.com/free/) today.

* Azure CLI and ML extension. For more information, see [Install, set up, and use the CLI (v2) (preview)](how-to-configure-cli.md). 

* An Azure ML compute cluter resource in your workspace in any of the [supported regions](#supported-regions), created post September 2021. Learn how to [create an Azure Machine Learning compute cluster](https://docs.microsoft.com/azure/machine-learning/how-to-create-attach-compute-cluster?tabs=python). 

## Supported regions

During the private preview, the Azure ML notebook-up feature is available in the following regions:

* East US2 EUAP
* West Central US
* East US
* East US 2
* North Europe
* South Central US

## Get started 

Now you have installed and set up the CLI v2, you can use the `az ml notebook up` for your model development. 

### Get the Azure ML CLI extension with Notebook-up support

The notebook-up feature is available via a private wheel file. To install it, follow these steps:

Remove the Azure ML CLI extension, if you have it installed already:
```shell
az extension remove --name ml
```

Install the private Azure ML CLI extension with notebook-up support:
```shell
az extension add --source https://azuremlsdktestpypi.blob.core.windows.net/wheels/azureml-v2-cli-e2e-test/49246860/ml-0.0.49246860-py3-none-any.whl --pip-extra-index-urls https://azuremlsdktestpypi.azureedge.net/azureml-v2-cli-e2e-test/49246860 -y
```

Verify your installation:
```shell
az extension list
```
You should see an extension with name "ml" in the output.


### Create compute in CLI

You can create an Azure Machine Learning compute cluster from the command line. For instance, the following commands will create one cluster named `cpu-cluster`.
```dotnetcli
az ml compute create -n cpu-cluster --type amlcompute --min-instances 0 --max-instances 10 
```
Note that you are not charged for compute at this point as `cpu-cluster` will remain at 0 nodes until a job is submitted. Learn more about how to [manage and optimize cost for AmlCompute](how-to-manage-optimize-cost.md#use-azure-machine-learning-compute-cluster-amlcompute).

The following example in this article use `cpu-cluster`. Adjust these as needed to the name of your cluster.

Use `az ml compute create -h` for more details on compute create options. Note that if you re-use an existing Azure ML compute cluster, it must have been created post September 2021 to support the notebook feature.

### Create a new notebook 

Having installed the [private Azure ML CLI extension](#Get-the-azure-ml-cli-extension-with-notebook-up-support) and [created a compute target](#create-compute-in-cli), execute the following command to launch a new notebook:
```shell
az ml notebook up --compute cpu-cluster
```

The command will launch a notebook job onto your compute target. It will also output a notebook job name and a URL to access the notebook. Opening the URL in a brower, you will be prompted for login credentials. At this point, only the user who has created the notebook is granted to access it. During private preview, the notebook will run for 20 minutes and will be automatically shutdown afterwards.

Note: if the command output showed the job is in `Queued` state for a long time, check that your compute target has an available node with no jobs running on it.

Additionally, you can provide a source folder for your notebook source code via the `--code` argument as follows:
```shell
az ml notebook up --compute cpu-cluster --code src/
```

During the execution of the command above, the content of the `src/` folder will be uploaded to your workspace's default storage account and will be available to in notebook at runtime.

You can also place a `requirements.txt` file in your source folder with the list of python packages that need to be installed in your python runtime. If you use pip locally, you can typically populate the content of `requirements.txt` file by running:
```shell
pip freeze > src/requirements.txt
```


### Stop a running notebook

You can stop a running notebook via the following command:

```shell
az ml notebook down --name <notebook_name>
```

You can find the name of your notebook job in the output of the command you used to create the notebook.

Alternatively, you can use the following command to list all notebooks that have been launched in your workspace:

```shell
az ml notebook list
```

### Cleanup

Consider resizing your AML compute cluster to zero nodes if it's not used. For this purpose, navigate to your workspace's *Compute* tab, select your cluster under *Compute clusters*, and edit the *Minimum number of nodes* under *Resource properties*.


## Coming soon

* Support distributed training with multi-nodes compute.
* Support clusterless compute as default compute to start with in case you don't have an existing compute. 
* Connect to VS Code using `az ml vscode up`. 
