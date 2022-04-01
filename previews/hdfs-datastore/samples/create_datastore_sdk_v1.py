# This code sample shows how to register a new Hdfs data store.  Please
# be sure to fill in the configuration properties below before running.

from azureml.core import Workspace, Datastore

workspace = Workspace.from_config()

datastore_name = "hdfs_datastore"
protocol = "https"
namenode_address = "<insert_namenode_address>"
hdfs_server_certificate = "</path/to/server/certificate>"
kerberos_realm = "<krb_realm>"
kerberos_kdc_address = "<insert_kdc_address>"
kerberos_principal = "<krb_principal>"
kerberos_keytab = "</path/to/keytab>"

datastore = Datastore.register_hdfs(
    workspace = workspace,
    datastore_name = datastore_name,
    protocol = protocol,
    namenode_address = namenode_address,
    hdfs_server_certificate = hdfs_server_certificate,
    kerberos_realm = kerberos_realm,
    kerberos_kdc_address = kerberos_kdc_address,
    kerberos_principal = kerberos_principal,
    kerberos_keytab = kerberos_keytab,
    kerberos_password = None,
    overwrite = True
)

print(datastore)
