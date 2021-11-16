# Overview

This file will provide a complete example of `AutoMLConfig` and some mock data required for running NER scenario.

# Example `AutoMLConfig`
set `task='text-ner'`
```
automl_settings = {
    "iterations": 1,
    "primary_metric": 'accuracy',
    "max_concurrent_iterations": 1,
    "featurization": 'auto',
    "enable_dnn": True,
    "verbosity": logging.INFO
}
automl_config = AutoMLConfig(task = 'text-ner', 
                             debug_log = 'automl_errors.log',
                             compute_target=compute_target,
                             training_data = train_data,
                             validation_data = val_data,
                             label_column_name = 'labels'
                             **automl_settings
                            )
```

# Mock Data

* Each sample should be splited into as many rows as needed, with each token taking a row with its label, separated with a space.
* Use a blank line to separate two samples
* A two sample example

```
The O
former O
Soviet B-MISC
republic O
was O
playing O
in O
an O
Asian B-MISC
Cup I-MISC
finals O
tie O
for O
the O
first O
time O
. O

It O
was O
the O
second O
costly O
blunder O
by O
Syria B-LOC
in O
four O
minutes O
. O
```