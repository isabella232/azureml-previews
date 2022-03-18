# Network isolation support for managed online endpoints

Our enterprise customers want to ensure their ML deployments are secure. With this preview we are enabling the following scenarios. 
1. Secure ingress via workspace Private Endpoint (PE) support: Once you deploy a model, the model serving endpoint (scoring_uri) can be configured to be accessed only from a private IP from your vnet. i.e. you will be able to use your Azure ML workspace Private Endpoint to access the scoring_uri of the managed online endpoint.
2. Secure egress via PEs to workspace resources: Egress from the scoring model container will be restricted only to specific resources via secure conectivity through PEs. Internet access is disabled.

Key benefits to the users are:
1. Secure connectivity helps with Data Exfiltration Protection.
2. No additional configuration is needed in user's VNET/NSG.

## Concept

![High Level Architecture](./media/vnet_architecture.jpg)

With workspace PE support, you can secure the ingress by creating a [PE to the workspace](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-configure-private-link?tabs=azurecliextensionv2).

With secure egress support, PE's are created from the managed endpoint deployment to workspace resources including ACR, KeyValut, Workspace, Filestore & Blob store. Internet access is not permitted. 

When you create managed online deployments you have the option of setting a flag `private_network_connection true`. Now all system communication will use the PEs (downloading model, code, images etc to the container). Any user logic leveraging these resources will also use the PEs. No additional configuration in user’s vnet are required.

This is the syntax to create a managed online deployment with secure egress.
```bash
az ml online-deployment create -f deployment.yml --set private_network_connection true
```

Creation and deletion of PEs to workspace resources are handled transparently along with the deployment.

Visibility of the scoring endpoint is governed by the [workspace flag `public_network_access`](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-configure-private-link?tabs=azurecliextensionv2#enable-public-access). If it is `disabled` then scoring endpoints can be accessed only from VNETs that have PEs to the workspace. If it is enabled, the scoring endpoints can be accessed both from the PEs and public networks.

__Note__: During this preview private endpoints to workspace resources are created per deployment - not per workspace as shown in the above diagram

### Supported scenarios

|Workspace property | Deployment property | Supported?|
|----------------|----------------------------------|---|
| `public_access_enabled` is Enabled| `private_network_connection` is false (default) | Yes |
| `public_access_enabled` is Disabled| `private_network_connection` is true) | Yes |


__Warning:__
1. If you create a deployment with `private_network_connection true`, the workspace flag `public_access_enabled` will automatically be changed to `Disabled`
1. If workspace public_network_access gets disabled for a workspace with existing public managed endpoints, then (a) the endpoints will not be publicly accessable (b) the public deployments will start failing

## End to end example
### Step 1: Prerequisites
* This private preview is by __invite only__ at this time. The subscription id and tenant id needs to be added to our allow-list.
* Install and configure the Azure CLI and the ml extension to the Azure CLI. For more information, see [Install, set up, and use the CLI (v2) (preview)](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-configure-cli). 
* You must have an Azure resource group, and you (or the service principal you use) must have Contributor access to it. A resource group is created in [Install, set up, and use the CLI (v2) (preview)](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-configure-cli).
* If you haven't already set the defaults for the Azure CLI, save your default settings. To avoid passing in the values for your subscription and resource group multiple times, run this code:
    ```bash
    az account set --subscription <subscription ID>
    az configure --defaults group=<resource group>
    ```
* Configure to access private preview feature from CLI:

    To activate the private feature enable it through environment variable (bash):
    ```bash
    export AZURE_ML_CLI_PRIVATE_FEATURES_ENABLED=true
    ```
    for powershell:
    ```
    $Env:AZURE_ML_CLI_PRIVATE_FEATURES_ENABLED=$true
    ```
     To deactivate either set the value to false or delete the environment variable.
* ACR needs to be premium SKU. If you use the below workspace setup script, this will be handled.

### Prepare your system
Clone the azureml-examples repo and navigate to the working folder.
```bash
git clone --branch rsethur/mvnet https://github.com/Azure/azureml-examples
cd azureml-examples/cli
```
   

### Step 2: Create secure workspace
If you have your own secure workspace setup, you could use that. Alternatively the below template will create the complete setup required for testing this feature:
![Sample setup](./media/vnet_sample_deployment_arch.jpg)
```bash
# SUFFIX will be used as resource name suffix in created workspace and related resources
export SUFFIX="<UNIQUE_SUFFIX>"
# This bicep template sets up secure workspace and relevant resources
az deployment group create --template-file endpoints/online/managed/vnet/setup/main.bicep --parameters suffix=$SUFFIX
```
The following resources will be created:
1. Azure ML workspace with public_network_access as disabled
2. ACR, storage and keyvault with public access disabled
3. A user vnet that will be used for scoring. Private endpoints will be created from this VNET to the above resources: Azure ML workspace, ACR, Keyvault, File and Blob stores.
4. A scoring subnet (snet-scoring) will be created with the outbound NSG rules as shown in the above picture. Internet outbound is enabled to get access to anaconda/pypi, get access to azureml-examples repo and download azure cli. You can disable it based on your needs.

Review the bicep template if you would like to understand more details.

The following resources will be created by you in the following steps:
1. Scoring VM
2. Managed endpoint 


Note: If you are not using the above template, then create private endpoint from your vnet to azure ml workspace using instructions [here]((https://docs.microsoft.com/en-us/azure/machine-learning/how-to-configure-private-link?tabs=azurecliextensionv2))

### Step 3: Setup a VM inside the vnet
We need to create a VM in the scoring subnet (snet-scoring), inorder to create and test a managed endpoint from within your vnet. 

```bash
# create vm
az vm create --name test-vm --vnet-name vnet-$SUFFIX --subnet snet-scoring --image UbuntuLTS --admin-username azureuser --admin-password <your-new-password>
# ssh into the vm: use the publicIpAddress that is output from the above steo
ssh azureuser@<vm_public_ip>
```
Note: the above script creates a VM with public IP for sake of simplfying this example. If you want a more secure VM setup, please go through [`az vm create` docs](https://docs.microsoft.com/en-us/cli/azure/vm?view=azure-cli-latest#az-vm-create). Basic vm creation tutorial is [here](https://docs.microsoft.com/en-us/azure/virtual-machines/linux/quick-create-cli)

Note: Execute rest of the steps from the SSH connection to the VM.

Setup the VM
```bash
# setup docker
sudo apt-get update -y && sudo apt install docker.io -y && sudo snap install docker && docker --version && sudo usermod -aG docker $USER
# setup az cli and ml extension
curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash && az extension add --upgrade -n ml -y
```

Setup environment variables
```bash
export SUBSCRIPTION="<YOUR_SUBSCRIPTION_ID>"
export RESOURCE_GROUP="<YOUR_RESOURCE_GROUP>"
export LOCATION="<LOCATION>"
# SUFFIX used during the initial setup. Alternatively the resource names can be looked up from the resource group after the  setup script has completed.
export SUFFIX="<SUFFIX_USED_IN_SETUP>"
export WORKSPACE=mlw-$SUFFIX
export ACR_NAME=cr$SUFFIX
export WORKSPACE=mlw-$SUFFIX
export ENDPOINT_NAME="<YOUR_ENDPOINT_NAME>"
```

Login using az cli. Alternatively you can use [service principal based authentication](https://docs.microsoft.com/en-us/cli/azure/authenticate-azure-cli#sign-in-with-a-service-principal).
```bash
# Login using az cli. This will ask you to sign in using the browser.
az login
```

Configure CLI defaults
```bash
az account set --subscription $SUBSCRIPTION
az configure --defaults group=$RESOURCE_GROUP workspace=$WORKSPACE location=$LOCATION
```

Clone the azureml-examples repo again - but inside the VM now. This is needed to build the image and create the managed online deployment.
```bash
sudo mkdir -p /home/samples; sudo git clone --branch rsethur/mvnet --depth 1 https://github.com/Azure/azureml-examples.git /home/samples/azureml-examples -q
```

### Step 4: Build the docker image that will be used by the managed endpoint deployment
Since internet egress is not allowed, we need to have a fully built image in ACR.

```bash
# Navigate to the samples
cd /home/samples/azureml-examples/cli/endpoints/online/managed/vnet/environment
# login to acr. Optionally, to avoid using sudo, complete the docker post install steps: https://docs.docker.com/engine/install/linux-postinstall/
sudo az acr login -n $ACR_NAME
# Build the docker image with the sample docker file
sudo docker build -t $ACR_NAME.azurecr.io/repo/img:v1 .
# push the image to the ACR
sudo docker push $ACR_NAME.azurecr.io/repo/img:v1
# check if the image exists in acr
az acr repository show -n $ACR_NAME --repository repo/img
```
As you will see in the next step, we will be using custom [container support](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-deploy-custom-container), to deploy this custom built image into managed endpoints.

#### Alternate option
Alternatively, you can build the docker image in your vnet using azure ml compute cluster and azure ml environments. Instructions [here](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-secure-workspace-vnet?tabs=pe%2Ccli#enable-azure-container-registry-acr).

### Step 5: Create managed online endpoint and deployment
We will use the example [here](https://docs.microsoft.com/en-us/azure/machine-learning/how-to-deploy-managed-online-endpoints#deploy-to-azure) to create the endpoint and deployment

```bash
# navigate to the cli directory in the azurem-examples repo
cd /home/samples/azureml-examples/cli/
# enable private preivew features in cli
export AZURE_ML_CLI_PRIVATE_FEATURES_ENABLED=true
# create endpoint
az ml online-endpoint create --name $ENDPOINT_NAME -f endpoints/online/managed/vnet/endpoint.yml
# create deployment with private_network_connection="true"
az ml online-deployment create --name blue --endpoint $ENDPOINT_NAME -f endpoints/online/managed/vnet/blue-deployment-vnet.yml --all-traffic --set environment.image="$ACR_NAME.azurecr.io/repo/img:v1" private_network_connection="true"
```

Note the flag  `--set private_network_connection true`.

Now you can test scoring using the `invoke` command from the cli or using curl
```bash
# Try scoring using the CLI
az ml online-endpoint invoke --name $ENDPOINT_NAME --request-file endpoints/online/managed/vnet/sample-request.json

# Try scoring using curl
ENDPOINT_KEY=$(az ml online-endpoint get-credentials -n $ENDPOINT_NAME -o tsv --query primaryKey)
SCORING_URI=$(az ml online-endpoint show -n $ENDPOINT_NAME -o tsv --query scoring_uri)
curl --request POST "$SCORING_URI" --header "Authorization: Bearer $ENDPOINT_KEY" --header 'Content-Type: application/json' --data @endpoints/online/model-1/sample-request.json
```

Note: If you use workspace PE, then you need to execute the above commands from within your VNET.
