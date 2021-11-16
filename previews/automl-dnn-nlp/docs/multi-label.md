# Overview

This file will provide a complete example of `AutoMLConfig` and some mock data required for running multi-label classification scenario.

# Example `AutoMLConfig`
set `task='text-classification-multilabel'`
```
automl_settings = {
    "iterations": 1,
    "primary_metric": 'accuracy',
    "max_concurrent_iterations": 1,
    "featurization": 'auto',
    "enable_dnn": True,
    "verbosity": logging.INFO,
}
automl_config = AutoMLConfig(task = 'text-classification-multilabel', 
                             debug_log = 'automl_errors.log',
                             compute_target = compute_target,
                             training_data = train_dataset,
                             validation_data = validation_dataset,
                             label_column_name = 'labels',
                             **automl_settings
                            )
```

# Mock Data

* Each row corresponds to one sample, all labels in a list
* A Three row example in csv format, classes are the sports mentioned in the text

```
text,labels
"I love watching Chicago Bulls games.","['basketball']"
"The four most popular leagues are NFL, MLB, NBA and NHL","['football','baseball','basketball','hockey']"
"I like drinking beer.","[]"
``` 