# Compute Instance Managed Identity

## How it works

You can create a compute instance with managed identity enabled. This feature is useful in a case where users should have restricted access to data, only from the compute instance, but not directly as Azure AD users. Also, you can simplify and reduce the number of role assignments by creating a user-assigned managed identity to access a common storage account, and assigning that identity to many compute instances. 

 The compute instance manged identity can be configured either using Azure Machine Learning Studio, or [template-based deployment](https://docs.microsoft.com/azure/templates/microsoft.machinelearningservices/workspaces/computes).

In Studio, navigate to **Compute** tab, select **Compute Instances**, and select **+New**. Fill in the required settings, and select **Advanced Settings**. Then, enable **Assign Managed Identity** and select the type of identity you intend to use. Finally, select **Create** to start the compute instance.

To use the managed identity to access data stores, go to compute instance properties, and note the identity principal Id.
Grant the managed identity required roles on the storage account, such as *Storage Blob Data Contributor* or *Storage Blob Data Reader*. For details on which storage systems support identity-based access, see [Connect to storage by using identity-based data access](https://docs.microsoft.com/azure/machine-learning/how-to-identity-based-data-access).

Once configured, the managed identity is used by default when accessing Azure Machine Learning data stores, except the workspace default data store for which user Azure AD identity is used.

Note that updating managed identity forces the compute instance to restart.

## Enrolling to private preview

Contact Roope Astala (roastala), and provide customer use case and Azure subscription ID for allow-listing.
