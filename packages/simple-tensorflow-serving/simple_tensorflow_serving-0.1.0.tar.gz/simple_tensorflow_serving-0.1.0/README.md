# Simple TensorFlow Serving

## Introduction

The simpler and easy-to-use serving service for TensorFlow models. 
 
* [x] Support TensorFlow SavedModel
* [x] Support the RESTful/HTTP APIs
* [x] Support `curl` and command-line tools 
* [x] Support clients in any programing language
 
## Installation



## Server


```
simple_tensorflow_serving --port=8500 --model_base_path="../examples/tensorflow_template_application_model/1/"
```


## Client

```
curl -H "Content-Type: application/json" -X POST -d '{"keys": [[11.0], [2.0]], "features": [[1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1]]}' http://127.0.0.1:8500
```

![]()

