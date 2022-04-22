# Create and run machine learning pipelines using components with the Azure ML Python SDK (v2) (preview)

In this article, you learn how to create and run machine learning pipelines by using the Azure ML Python SDK (v2). AzureML Pipelines may be defined in YAML and run from the CLI, authored in Python SDK (v2), or composed in AzureML Studio Designer with a drag-and-drop UI. This document focuses on Python SDK (v2).

## Prerequisites

* If you don't have an Azure subscription, create a free account before you begin. Try the [free or paid version of Azure Machine Learning](https://azure.microsoft.com/free/) today
* The Azure Machine Learning SDK v2 for Python - [install SDKv2](install-sdkv2.md)
* An Azure Machine Learning workspace

### Clone examples repository

To run the training examples, first clone the examples repository and change into the `sdk` directory:

```bash
git clone --depth 1 https://github.com/Azure/azureml-examples --branch sdk-preview
cd azureml-examples/sdk
```

All the files and code used in this document are available in `jobs/pipelines/e2epipelinesample` folder.

## Introducing machine learning pipelines

Pipelines in Azure Machine Learning let you sequence a collection of machine learning tasks into a workflow. Data Scientists typically iterate with scripts focusing on individual tasks such as data preparation, training, scoring, and so forth. When all these scripts are ready, pipelines help connect a collection of such scripts into production-quality processes.

In this example we will be building a pipeline which performs 5 tasks:

* Prepare Data
* Transform Data
* Train a regression model
* Test using the model
* Score using the model

The end result will look like this
:::image type="content" source="media/pipeline-structure.jpg" alt-text="Pipeline Structure":::

Each of the above steps will be constructed as a component. A component is similar to a command as seen in [train models](train-sdkv2.md) sample. However, components are reusable because they define placeholders for input and output parameters instead of predefined values. The input output values can be provided when constructing the pipleine. For more details, see [What is an Azure Machine Learning component?](https://docs.microsoft.com/azure/machine-learning/concept-component). 

## Build the pipeline

Let us look how to construct this pipeline. 
### Prepare Data

The first step is to load the data. We will do this using a component to load data.

```python
from azure.ml import command, Input, Output
prepare_data = command(
    code="./prep_src",
    command="python prep.py --raw_data ${{inputs.raw_data}} --prep_data ${{outputs.prep_data}}",
    environment="AzureML-sklearn-0.24-ubuntu18.04-py37-cpu@latest",
    inputs={"raw_data": Input(type="uri_folder")},
    outputs={"prep_data": Output(type="uri_folder")},
    name="prepare_taxi_data",
    display_name="PrepTaxiData"
)
```

As explained before, the `prepare_data` component is created using a `command`. The difference is that:

1. Inputs and Outputs are defined as a type, but no actual values are provided. A default value can be provided if needed.
1. A compute is not associated with the command. A compute will be allocated when constructing the pipeline.

### Transform Data

To transform data, we will create a component, but instead of loading it by writing python code (refer the prepare data step above), we will load it by using a `YAML` file. A component can be defined in a YAML format. To transform data we will use the `transform.yml` file. Let us examine this file:

```YAML
$schema: https://azuremlschemas.azureedge.net/latest/commandComponent.schema.json
name: taxi_feature_engineering
display_name: TaxiFeatureEngineering
version: 1
type: command
inputs:
  clean_data: 
    type: uri_folder 
outputs:
  transformed_data:
    type: uri_folder
code: ./transform_src
environment: azureml:AzureML-sklearn-0.24-ubuntu18.04-py37-cpu@latest
command: >-
  python transform.py 
  --clean_data ${{inputs.clean_data}} 
  --transformed_data ${{outputs.transformed_data}}
```

As can be seen, the YAML format structure is similar to the python code to define a command. In fact, this is what allows the YAML to be loaded as a compnent in python. To load this yaml file into a component we will use the following code:

```python
from azure.ml.entities import load_component
transform_data = load_component(yaml_file="./transform.yml")
```

The advantage of using a YAML file is that it can be stored and shared easily across users and workspaces.

### Train Model and other steps

We will use YAML files to load 3 other components.

```python
from azure.ml.entities import load_component
train_model = load_component(yaml_file="./train.yml")
predict_result = load_component(yaml_file="./predict.yml")
score_data = load_component(yaml_file="./score.yml")
```

### Construct the pipeline

Now that we have all the indivudual pieces ready, we will construct a pipeline by stringing them together. The individual pieces are connected to each other using inputs and outputs. To construct the pipeline we will use the `dsl` or Domain Specific Language of Azure ML. Refer the documentation [here](https://review.docs.microsoft.com/python/api/azure-ml/azure.ml.dsl?view=azure-ml-py&branch=sdk-cli-v2-preview-master) for more details.

```python
from azure.ml import dsl
@dsl.pipeline(default_compute="cpu-cluster", default_datastore="workspaceblobstore")

def nyc_taxi_data_regression(pipeline_job_input):
    prepare_sample_data = prepare_data(raw_data=pipeline_job_input)
    transform_sample_data = transform_data(
        clean_data=prepare_sample_data.outputs.prep_data
    )
    train_with_sample_data = train_model(
        training_data=transform_sample_data.outputs.transformed_data
    )
    predict_with_sample_data = predict_result(
        model_input=train_with_sample_data.outputs.model_output,
        test_data=train_with_sample_data.outputs.test_data,
    )
    score_with_sample_data = score_data(
        predictions=predict_with_sample_data.outputs.predictions,
        model=train_with_sample_data.outputs.model_output,
    )
    return {
        "pipeline_job_prepped_data": prepare_sample_data.outputs.prep_data,
        "pipeline_job_transformed_data": transform_sample_data.outputs.transformed_data,
        "pipeline_job_trained_model": train_with_sample_data.outputs.model_output,
        "pipeline_job_test_data": train_with_sample_data.outputs.test_data,
        "pipeline_job_predictions": predict_with_sample_data.outputs.predictions,
        "pipeline_job_score_report": score_with_sample_data.outputs.score_report,
    }
```

Let us examine the code. In this line, the compute and storage needed to run the pipeline is defined.

```python
@dsl.pipeline(default_compute="cpu-cluster", default_datastore="workspaceblobstore")
```

AFter this we define the pipeline as a function called `nyc_taxi_data_regression`. All the components we created used as functions within the `nyc_taxi_data_regression`. The output of one function is passed on as input to another function, this building a dependency of steps and also determining the order in which they will run. This can be seen by examining the first few lines of the definition of `nyc_taxi_data_regression`.

```python
def nyc_taxi_data_regression(pipeline_job_input):
    prepare_sample_data = prepare_data(raw_data=pipeline_job_input)
    transform_sample_data = transform_data(
        clean_data=prepare_sample_data.outputs.prep_data
    )
    ....
```

### Define the input data to the pipeline

The `nyc_taxi_data_regression` expects an input `pipeline_job_input`. We will send our input data using this input parameter. Let us define the input data.

```python
pipeline = nyc_taxi_data_regression(
    Input(type="uri_folder", path="./data/")
)
```

### Run the pipeline
Now that we have constrcuted the pipeline, let us run the pipeline. To run the pipeline, we first need to connect to a workspace.

#### 1. Connect to the workspace

To connect to the workspace, we need identifier parameters - a subscription, resource group and workspace name. We will use these details in the `MLClient` from `azure.ml` to get a handle to the required Azure Machine Learning workspace. To authenticate, we use the [default azure authentication](https://docs.microsoft.com/python/api/azure-identity/azure.identity.defaultazurecredential?view=azure-python). Check this [example](https://github.com/Azure/azureml-examples/blob/sdk-preview/sdk/jobs/configuration.ipynb) for more details on how to configure credentials and connect to a workspace.

<!--[!notebook-python[] (~/azureml-examples/blob/sdk-preview/sdk/jobs/single-step/lightgbm/iris/lightgbm-iris-sweep.ipynb?name=connect-workspace)]-->

```python
#import required libraries
from azure.ml import MLClient
from azure.identity import DefaultAzureCredential

#Enter details of your AML workspace
subscription_id = '<SUBSCRIPTION_ID>'
resource_group = '<RESOURCE_GROUP>'
workspace = '<AML_WORKSPACE_NAME>'

#connect to the workspace
ml_client = MLClient(DefaultAzureCredential(), subscription_id, resource_group, workspace)
```

#### 2. Create compute

We will create a compute called `cpu-cluster` for our pipeline. This was the name used while defineing the pipeline. This is done as follows:

<!--[!notebook-python[] (~/azureml-examples/blob/sdk-preview/sdk/jobs/configuration.ipynb?name=create-cpu-compute)]-->

```python
from azure.ml.entities import AmlCompute

# specify aml compute name.
cpu_compute_target = 'cpu-cluster'

try:
    ml_client.compute.get(cpu_compute_target)
except Exception:
    print('Creating a new cpu compute target...')
    compute = AmlCompute(name=cpu_compute_target, size="STANDARD_D2_V2", min_instances=0, max_instances=4)
    ml_client.compute.begin_create_or_update(compute)
```

#### 3. Run the pipeline

We will use the `ml_client` to run the pipeline.

```python
pipeline_job = ml_client.jobs.create_or_update(pipeline)
pipeline_job.services["Studio"].endpoint
```

The run of this pipeline can be monitored and seen using the link displayed in the above step.  We have now succesfully run a pipeline which performs 5 steps:

* Prepare Data
* Transform Data
* Train a regression model
* Test using the model
* Score using the model

## Next Steps

Try these next steps to learn how to use the Azure Machine Learning SDK (v2) for Python:

1. [Deploy Models with the Azure ML Python SDK (v2) (preview)](deploy-models-sdkv2.md)
1. [Train models with the Azure ML Python SDK (v2) (preview)](train-sdkv2.md)
