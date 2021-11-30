## QuickStart
This guide helps you quickly explore the main features of AzureML - Delta Lake integration. It provides code snippets that show how to read from a Delta tables on to an AzureML Dataset and subsequently load the data on to a Pandas dataframe. The Delta Lake tables (data) can be in any one of the following storage accounts –
1. ADLS Gen2
2. Blobstore
3. File Share

In this article:
* What’s New in Azure Machine Learning for Delta Lake?
* Setup AzureML Compute Instance with a Notebook to integrate with a Delta Lake Datastore 
* Import the right packages and Configuration
* Datastore, Folder path and Permissions
* Create a Dataset from a Datastore with “timestamp_as_of” option and Time-travel 
* Create a Dataset from a Datastore with “version_as_of” option and Time-travel 
* Load the Dataset on to Pandas dataframe

### What’s New in Azure Machine Learning for Delta Lake 
Azure Machine Learning Dataset SDK has a new method under Tablular Dataset called – “from_delta_lake”

This new method takes one the following as inputs:
1. path and timestamp                   
   OR  
2. path and version 

The path consists of the Datastore and folder path to the folder which contains “_delta_log” folder and the timestamp or version for "Time-travel"

Signature would look like this:
```
Dataset.Tabular.from_delta_lake(path=(ds, path_datastore), timestamp_as_of=timestamp)
```
```
Dataset.Tabular.from_delta_lake(path=(ds, path_datastore), version_as_of=version_as_of)
```

### Setup AzureML Compute Instance with a Notebook to integrate with a Delta Lake Datastore

Follow these instructions to set up Delta Lake integration with AzureML. You can run the steps in a Compute Instance - Notebook:

Install the AzureML SDK versions that is compatible with the Delta Lake by running the following:
```
!pip uninstall --yes azureml-dataprep azureml-dataprep-native azureml-dataprep-rslex azureml-core 

!pip install azureml-dataprep[pandas] --index https://dataprepdownloads.azureedge.net/pypi/test-M3ME5B1GMEM3SW0W/46761121/ --no-deps 

!pip install azureml-dataprep-rslex --index https://dataprepdownloads.azureedge.net/pypi/test-M3ME5B1GMEM3SW0W/46761121/ --no-deps 

!pip install azureml-dataprep-native --index https://dataprepdownloads.azureedge.net/pypi/test-M3ME5B1GMEM3SW0W/46761121/ --no-deps 

!pip install azureml-core --index https://azuremlsdktestpypi.azureedge.net/Create-Dev-Index/51809517/ --no-deps

!pip show azureml-dataprep azureml-dataprep-rslex azureml-dataprep-native azureml-core 
```
>[!TIP]
> You have to restart the Kernel after installing the appropriate SDK version (using the above step).

### Import the right packages and Configuration
To import the required packages and configuration – run the following:
```
from azureml.core import Datastore, Workspace, Dataset 
from azureml.data.datapath import DataPath 

ws = Workspace.from_config() 
```
To check the Workspace that has been loaded from the configuration, run the following: 
```
print('Workspace name: ' + ws.name, 
      'Azure region: ' + ws.location,
      'Subscription id: ' + ws.subscription_id,
      'Resource group: ' + ws.resource_group, sep='\n') 
```
>[!TIP]
> This should be the Azure ML workspace which has the Datastore that has the Delta Lake files loaded.

### Datastore, Folder path and Permissions
Azure Machine Learning, Currently supports integrating with Delta Lake data in the following storage options:
* ADLS Gen 2
* Blobstore
* File Share

In order to use Data Lake data in Azure Machine Learning, an AzureML Datastore needs to be created with one of the above "Datastore types".
The created Datastore which has the Delta lake files will be referenced by its appropriate name while creating a Dataset.

>[!NOTE]
> 1. If using ADLS Gen2 Storage, have *Hierarchical Namespace Enabled*.
> 2. A Role – *“Storage Blob Data Reader”* or *“Storage Blob Data Contributor”* needs to be associated to the AzureML Workspace “Managed Identity” in the Storage Account that has the Delta Lake data in ADLS Gen 2 or Blobstore or Fileshare.



>[!TIP]
 > Note the name of parent folder in the storage account which has *“_delta_log”* folder where the Delta Lake data files have been uploaded, the parent folder name needs to be referenced while creating the Dataset by referencing the path.

### Create a Dataset from a Datastore with “timestamp_as_of” option and Time-travel
To create a Azure ML Dataset referencing the Datastore which has Delta Lake files uploaded and a timestamp, You can run the following code by substituting the below:

```python
ds = Datastore.get(ws, "<name_of_the_data_store>") 
path_datastore = "<name_of_the_folder>" 
timestamp = "YYYY-MM-DDTHH:MM:SSZ" 
<my_aml_dellake_dataset> = Dataset.Tabular.from_delta_lake(path=(ds, path_datastore), timestamp_as_of=timestamp)
```

### Create a Dataset from a Datastore with “version_as_of” option and Time-travel
To create a Azure ML Dataset referencing the Datastore which has Delta Lake files uploaded and a version, You can run the following code by substituting the below:

```python
ds = Datastore.get(ws, "<name_of_the_data_store>") 
path_datastore = "<name_of_the_folder>" 
version_as_of = <version_as_of> 
<my_aml_dellake_dataset> = Dataset.Tabular.from_delta_lake(path=(ds, path_datastore), version_as_of= version_as_of)
```

>[!TIP]
> **<name_of_the_data_store>** = Name of the Datastore that you have created selecting the appropriate “Datastore type” as ADLS Gen2 or Blobstore or File Share, where you have referenced the Store name and details where you have uploaded the Delta Lake files.
>
> **<name_of_the_folder>** = Name of parent folder in the storage account which has “_delta_log” folder where the Delta Lake data files have been uploaded and referenced above.
>
> **"YYYY-MM-DDTHH:MM:SSZ"** = **Eg: "2021-08-26T00:00:00Z"** = This can be current time, If you want the latest data and earlier time for “Time travel”.
>
> **<my_aml_dellake_dataset>** = The name of the Dataset that you want to be created.
> **<version_as_of>** = **Eg: 2** = This can be current version, If you know the current version and want the latest data and earlier versions for “Time travel”.

>[!NOTE]
> Each CRUD operation in the Delta Lake data creates a new version and the version number increases by 1. With the Oldest version having a version number = 1.     
> If there is no data with the version number specified, You will receive an error mentioning the same.

### Load the Dataset on to Pandas dataframe
You can load the AzureML Dataset that you created with the Delta Lake data on to a Pandas dataframe to be used in Notebook and use Pandas in your machine learning work.  

Use the following to load the Dataset on to Pandas dataframe:
```python
<my_aml_dellake_dataset>.to_pandas_dataframe()
```

You can see the values of the Dataset using the following:
```python
print(<my_aml_dellake_dataset>.to_pandas_dataframe())
```