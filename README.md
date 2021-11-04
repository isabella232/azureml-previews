# Azure Machine Learning previews

Welcome to the Azure Machine Learning previews repository!

## Prerequisites

1. An Azure subscription. If you don't have an Azure subscription, [create a free account](https://aka.ms/AMLFree) before you begin.
2. A terminal. [Install and set up the CLI (v2)](https://docs.microsoft.com/azure/machine-learning/how-to-configure-cli) before you begin.

## Public previews

Public preview examples can be found at https://github.com/Azure/azureml-examples/tree/main/cli. Documentation for v2 preview features is listed below.

Installation and set up:

- [Install and set up the CLI (v2)](https://docs.microsoft.com/azure/machine-learning/how-to-configure-cli)
- [Set up the VSCode extension](https://docs.microsoft.com/azure/machine-learning/how-to-setup-vs-code)

Train models (jobs):

- [Train models with the CLI (v2)](https://docs.microsoft.com/azure/machine-learning/how-to-train-cli) 

Deploy models (endpoints and deployments):

- [What are Azure Machine Learning endpoints?](https://docs.microsoft.com/azure/machine-learning/concept-endpoints)
- [Deploy and score a machine learning model with a managed online endpoint](https://docs.microsoft.com/azure/machine-learning/how-to-deploy-managed-online-endpoints)
- [Safe rollout for online endpoints](https://docs.microsoft.com/azure/machine-learning/how-to-safely-rollout-managed-endpoints)
- [Use managed online endpoints in the studio](https://docs.microsoft.com/azure/machine-learning/how-to-use-managed-online-endpoint-studio) 
- [Viewing costs for managed online endpoints](https://docs.microsoft.com/azure/machine-learning/how-to-view-online-endpoints-costs)
- [Managed online endpoints SKU list](https://docs.microsoft.com/azure/machine-learning/reference-managed-online-endpoints-vm-sku-list) 
- [Monitoring managed online endpoints](https://docs.microsoft.com/azure/machine-learning/how-to-monitor-online-endpoints)
- [Tutorial: Access Azure resources with a managed online nedpoint and system-managed identity](https://docs.microsoft.com/azure/machine-learning/tutorial-deploy-managed-endpoints-using-system-managed-identity)
- [Troubleshooting managed online endpoints](https://docs.microsoft.com/azure/machine-learning/how-to-troubleshoot-managed-online-endpoints)
- [Batch scoring with batch endpoints](https://docs.microsoft.com/azure/machine-learning/how-to-use-batch-endpoint)
- [Troubleshooting batch endpoints](https://docs.microsoft.com/azure/machine-learning/how-to-troubleshoot-batch-endpoints)

Reference:

- [CLI (v2) commands](https://docs.microsoft.com/cli/azure/ml?view=azure-cli-latest)
- [YAML schemas](https://docs.microsoft.com/azure/machine-learning/reference-yaml-overview)

## Private previews

**preview**|**description**
-|-
[pipelines](previews/pipelines)|Pipelines for the CLI (v2), defined through YAML specification
[interactive-job](previews/interactive-job)|Run an interactive job on Arc compute
[automl](https://github.com/Azure/AutoML-vNext-Preview)|AutoML for the CLI (v2), defined through YAML specification

## Contents

directory|description
-|-
`previews`|Self-contained directories of private previews

## Contributing

We welcome contributions and suggestions! Please see the [contributing guidelines](CONTRIBUTING.md) for details.

## Code of Conduct

This project has adopted the [Microsoft Open Source Code of Conduct](https://opensource.microsoft.com/codeofconduct/). Please see the [code of conduct](CODE_OF_CONDUCT.md) for details.
