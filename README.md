# Keras Bucket Tensorboard Callback

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PyPI version](https://badge.fury.io/py/keras-bucket-tensorboard-callback.svg)](https://badge.fury.io/py/keras-bucket-tensorboard-callback)
[![Maintainability](https://api.codeclimate.com/v1/badges/74540030ca0b44ff2dfb/maintainability)](https://codeclimate.com/github/neuronio-ai/keras_bucket_tensorboard_callback/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/74540030ca0b44ff2dfb/test_coverage)](https://codeclimate.com/github/neuronio-ai/keras_bucket_tensorboard_callback/test_coverage)

A Keras Callback that uploads your Tensorboard logs to a Cloud Bucket

*Currently, only Google Cloud Platform Storage is supported. Very little effort
is needed to support AWS S3, so feel free to contribute to this project.*

## Installation
```bash
pip install keras-bucket-tensorboard-callback
```

## Basic usage

The following example trains uploads the Tensorboard logs to you GCP Storage
bucket `my-bucket`, inside the directory `any_dir`:

```python
# Import the class
from keras_bucket_tensorboard_callback import BucketTensorBoard

# Create the callback instance, passing the bucket URI
bucket_callback = BucketTensorBoard('gs://my-bucket/any_dir')

# Train the model with the callback
model.fit(
    x=X,
    y=Y,
    epochs=20,
    callbacks=[bucket_callback]
)
```

Make sure you have access to the provided bucket. For GCP, you should have
the `GOOGLE_APPLICATION_CREDENTIALS` env set, pointing to your `json` key
file.

## Viewing the results on TensorBoard
With tensorboard installed your environment, run:
```bash
tensorboard --logdir=gs://my-bucket/any_dir
```

The TensorBoard will show your metrics and graphs saved on the bucket.