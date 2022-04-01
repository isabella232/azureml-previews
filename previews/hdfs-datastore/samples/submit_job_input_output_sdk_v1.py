import os
from azureml.core import Workspace, Datastore, Dataset, ComputeTarget, Environment, Experiment, ScriptRunConfig
from azureml.data import OutputFileDatasetConfig

workspace = Workspace.from_config()

# Get a reference to the existing Hdfs datastore
datastore_name = "<hdfs_datastore_name>"
datastore = Datastore.get(workspace, datastore_name)

# Create a dataset pointing at files in the datastore (used as training input)
input_dataset = Dataset.File.from_files(path = (datastore, "<path/to/files>"), validate = False)

# Optionally register the dataset
input_dataset.register(
    workspace = workspace,
    name = "hdfs_dataset",
    description = "This is a Hdfs test dataset.",
    tags = None,
)

# Create an output dataset reference (used for writing an output during training)
destination_path = "</path/to/destination>"
output_dataset = OutputFileDatasetConfig(destination = (datastore, destination_path))

# Get a reference to the existing AmlArc compute target
compute_target_name = "<amlarc_compute_target_name>"
compute = ComputeTarget(workspace, name = compute_target_name)

# Create an environment for training with the necessary dependencies installed
dockerfile_path = os.path.join(os.getcwd(), 'files', 'Dockerfile')
env = Environment.from_dockerfile(name = "hdfs-env", dockerfile = dockerfile_path)
env.python.user_managed_dependencies = True

# Create an experiment to collect training runs
experiment_name = "<experiment_name>"
exp = Experiment(workspace, experiment_name)

# Create the configuration for the training run
script_run_config = ScriptRunConfig(
    source_directory = 'files',
    script = 'read_write_script.py',
    arguments = [
        '--read-path',
        input_dataset.as_mount(),
        '--write-path',
        output_dataset.as_mount()
    ],
    compute_target = compute,
    environment = env
)

run = exp.submit(script_run_config)
print(run)
