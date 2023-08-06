import logging

import gen_bash
import gen_golang
import gen_javascript
import gen_python


def gen_tensorflow_sdk(tensorflow_inference_service, language):
  """
  Generate the TensorFlow SDK for programming languages.
  
  Args:
    tensorflow_inference_service: The tensorflow service object.
    language: The sdk in this programming language to generate.
    
  Return:
    None
  """

  if language not in ["bash", "python", "golang", "javascript"]:
    logging.error("Language: {} is not supported to gen sdk".format(language))
    return

  # Example: {"keys": [-1, 1], "features": [-1, 9]}
  input_opname_shape_map = {}

  for input_item in tensorflow_inference_service.model_graph_signature.inputs.items(
  ):
    # Example: "keys"
    input_opname = input_item[0]
    input_opname_shape_map[input_opname] = []

    # Example: [-1, 1]
    shape_dims = input_item[1].tensor_shape.dim

    for dim in shape_dims:
      input_opname_shape_map[input_opname].append(int(dim.size))

  logging.debug(
      "The input operator and shape: {}".format(input_opname_shape_map))

  # Example: {"keys": [[1.0], [2.0]], "features": [[1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1]]}
  generated_tensor_data = {}

  batch_size = 2
  for opname, shapes in input_opname_shape_map.items():

    # Use to generated the nested array
    internal_array = None

    # Travel all the dims in reverse order
    for i in range(len(shapes)):
      dim = shapes[len(shapes) - 1 - i]

      if dim == -1:
        dim = batch_size

      if internal_array == None:
        internal_array = [1.0 for i in range(dim)]
      else:
        internal_array = [internal_array for i in range(dim)]

    generated_tensor_data[opname] = internal_array

  if language == "bash":
    gen_bash.gen_tensorflow_sdk(generated_tensor_data)
  elif language == "python":
    gen_python.gen_tensorflow_sdk(generated_tensor_data)
  elif language == "golang":
    gen_golang.gen_tensorflow_sdk(generated_tensor_data)
  elif language == "javascript":
    gen_javascript.gen_tensorflow_sdk(generated_tensor_data)
