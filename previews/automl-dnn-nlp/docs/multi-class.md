# Overview

This file will provide a complete example of `AutoMLConfig` and some mock data required for running multi-class classification scenario.

# Example `AutoMLConfig`
set `task='text-classification'`
```
automl_settings = {
  "iterations": 1,
  "primary_metric": 'accuracy',
  "max_concurrent_iterations": 1,
  "featurization": 'auto',
  "enable_dnn": True,
  "verbosity": logging.INFO,
}
automl_config = AutoMLConfig(task = 'text-classification', 
                             debug_log = 'automl_errors.log',
                             compute_target = compute_target,
                             training_data = train_dataset,
                             validation_data = val_dataset,
                             label_column_name= 'labels',
                             **automl_settings
                            )
```

# Mock Data

* Each row corresponds to one sample 
* A Three row example in csv format, classes show if customers are satisfied (Although there is only one feature column, we support multiple feature columns)

```
text,labels
"The food is great!","Yes"
"The service should have been better.","No"
"I prefer the pizza from another restaurant.","No"
```