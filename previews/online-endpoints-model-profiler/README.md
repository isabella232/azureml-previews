# Online Endpoints Model Profiler

## Overview 

Inferencing machine learning models is a time and compute intensive process. It is vital to quantify the performance of model inferencing to ensure that you make the best use of compute resources and reduce cost to reach the desired performance SLA (e.g. latency, throughput).

Online Endpoints Model Profilier provides fully managed experience that makes it easy to benchmarch your model's performance served through [Online Endpoints](https://docs.microsoft.com/en-us/azure/machine-learning/concept-endpoints). 
* Use the benchmarking tool of your choice.
* Easy to use CLI experience.
* Support for CI/CD MLOps pipelines to automate profiling.
* Thorough performance report containing latency percentiles and resouce utilization metrics.

## Prerequisites

* Azure subscription. If you don't have an Azure subscription, sign up to try the [free or paid version of Azure Machine Learning](https://azure.microsoft.com/free/) today.

* Azure CLI and ML extension. For more information, see [Install, set up, and use the CLI (v2) (preview)](how-to-configure-cli.md). 

## Get started 

### Create an online endpoint

Follow the example in this [tutorial](how-to-deploy-managed-online-endpoints.md) to deploy a model using an online endpoint.

* Replace the `instance_type` in deployment yaml file with your desired Azure VM SKU. VM SKUs vary in terms of computing power, price and availability in different Azure regions.

* Tune `request_settings.max_concurrent_requests_per_instance` which defines the concurrent level. The higher this setting is, the higher throughput the endpoint gets. If this setting is set higher than the online endpoint can handle, the inference request may end up waiting in the queue and eventually results in longer end-to-end latency.

* If you plan to profile using multiple `instance_type` and `request_settings.max_concurrent_requests_per_instance`, please create one online deployment for each pair. You can attach all online deployments under the same online endpoint.

Below is a sample yaml file defines an online deployment.

:::code language="yaml" source="https://github.com/tracychms/profiling/blob/main/code/online-endpoint/blue-deployment-tmpl.yml" :::

### Create a compute to host the profiler

You will need a compute to host the profiler, send requests to the online endpoint and generate performance report. 

* This compute is not the same one that you used above to deploy your model. Please choose a compute SKU with proper network bandwidth (considering the inference request payload size and profiling traffic) in the same region as the online endpoint.

* Create proper role assignment for accessing online endpoint resources.

:::code language="azurecli" source="https://github.com/tracychms/profiling/blob/main/code/profiling/create-profiling-compute.sh" ID="create_compute_cluster_for_hosting_the_profiler" :::

:::code language="azurecli" source="https://github.com/tracychms/profiling/blob/main/code/profiling/create-profiling-compute.sh" ID="create role assignment for acessing workspace resources" :::

### Create a profiling job

#### Understand a profiling job

A profiling job simulates how an online endpoint serves live requests. It produces a throughput load to the online endpoint and generates performance report.

Below is a template yaml file defines a profiling job.

:::code language="yaml" source="https://github.com/tracychms/profiling/blob/main/code/profiling/profiling_job_tmpl.yml" :::

YAML syntax
| Key | Type  | Description | Allowed values | Default value |
| `environment.image` | string | An Azure Machine Learning curated image containing benchmarking tools and profiling scripts. | docker.io/rachyong/profilers:latest | |
| `environment_variables.ONLINE_ENDPOINT` | string | The online endpoint to be profiled. |  |  |
| `environment_variables.DEPLOYMENT` | string | The online deployment hosting the model to be profiled. |  |  |
| `environment_variables.PROFILING_TOOL` | string | The list of supported benchmarking tools. | `wrk`, `wrk2`, `labench` | `wrk` |
| `environment_variables.DURATION` | string | Period of time for running the benchmarking tool. Supported by `wrk`, `wrk2` and `labench`. |  | `300s` |
| `environment_variables.CONNECTIONS` | string | Number of connections for the benchmarking tool. Default value is set to be the number of `request_settings.max_concurrent_requests_per_instance`, or `WORKER_COUNT` in environment variables in online deployment, or 1 if both two values are not set or Null. Supported by `wrk` and `wrk2`. |  |  |
| `environment_variables.THREAD` | string | Number of threads allocated for the benchmarking tool. Supported by `wrk` and `wrk2`. |  | `1` |
| `environment_variables.TARGET_RPS` | string | Target reuest per second for the benchmarking tool. Supported by `wrk2` and `labench`. |  | `50` |
| `environment_variables.CLIENTS` | string | Number of clients for the benchmarking tool. Default value is set to be the number of `request_settings.max_concurrent_requests_per_instance`, or `WORKER_COUNT` in environment variables in online deployment, or 1 if both two values are not set or Null. Supported by `labench`. |  |  |
| `environment_variables.TIMEOUT` | string | Timeout in seconds for each request. Supported by `labench`. |  | `10s` |
| `inputs.payload` | string | The file of sampled payload containing a list of JSON objects that is stored in an AML registered datastore. |  |  |

#### Create a profiling job

Update the profiling job yaml template with your own values and create a profiling job.

:::code language="azurecli" source="https://github.com/tracychms/profiling/blob/main/code/profiling/how-to-profile-online-endpoint.sh" ID="create_profiling_job" :::

#### Read the performance report

## Coming soon

## Contact us

For any questions, bugs and requests of new features, please contact us at [mprof@microsoft.com](mailto:mprof@microsoft.com)