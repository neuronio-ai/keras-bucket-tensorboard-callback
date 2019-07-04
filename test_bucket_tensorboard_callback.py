import unittest
from os import listdir
from os.path import exists
from random import choice
from shutil import rmtree
from string import ascii_lowercase
from sys import argv
from tempfile import gettempdir

from google.cloud import storage
from keras.layers import Dense
from keras.models import Sequential
from numpy.random import rand, randint

from keras_bucket_tensorboard_callback import BucketTensorBoard


class TestBucketTensorboardCallback(unittest.TestCase):
    def test_logs_uploaded_gcp(self):
        # The callback we need to test
        bucket_uri = f"{self.bucket_uri.strip('/')}/{''.join([choice(ascii_lowercase) for i in range(10)])}"
        bucket_tb = BucketTensorBoard(bucket_uri)

        # Make sure that the temp dicretory does not exist
        logs_dir = f'{gettempdir()}/tensorboard_callbacks/{bucket_uri[5:]}'
        if exists(logs_dir):
            rmtree(logs_dir, ignore_errors=True)

        # Make sure that the cloud dicretory does not exist
        for blob in bucket_tb.bucket.list_blobs(prefix=bucket_uri[5:].split('/', 1)[1]):
            blob.delete()

        # Compile the model
        self.model.compile(
            optimizer='sgd',
            loss='binary_crossentropy',
            metrics=['accuracy']
        )

        # Train the model
        history = self.model.fit(
            x=self.X,
            y=self.Y,
            verbose=0,
            epochs=3,
            callbacks=[bucket_tb]
        )

        # Check if the model was trained for 3 epochs, so we can check if
        # tensorboard is showing all 3 epochs
        self.assertEqual(len(history.history['loss']), 3)
        self.assertEqual(len(history.history['acc']), 3)

        # Check if the temp directory has one file
        self.assertEqual(1, len(listdir(logs_dir)))

        # Check if the cloud directory has one file
        self.assertEqual(1, len(list(bucket_tb.bucket.list_blobs(
            prefix=bucket_uri[5:].split('/', 1)[1]))))

        # Train the model again
        self.model.fit(
            x=self.X,
            y=self.Y,
            verbose=0,
            epochs=3,
            callbacks=[bucket_tb]
        )

        # Check if the temp directory has two files
        self.assertEqual(2, len(listdir(logs_dir)))

        # Check if the cloud directory has two files
        self.assertEqual(2, len(list(bucket_tb.bucket.list_blobs(
            prefix=bucket_uri[5:].split('/', 1)[1]))))

        # Erase the logs dir
        logs_dir = f'{gettempdir()}/tensorboard_callbacks/{bucket_uri[5:]}'
        if exists(logs_dir):
            rmtree(logs_dir, ignore_errors=True)

        # Erase the bucket created files
        for blob in bucket_tb.bucket.list_blobs(prefix=bucket_uri[5:].split('/', 1)[1]):
            blob.delete()

         # Check if the temp directory has no files
        self.assertFalse(exists(logs_dir))

        # Check if the cloud directory has no files
        self.assertEqual(0, len(list(bucket_tb.bucket.list_blobs(
            prefix=bucket_uri[5:].split('/', 1)[1]))))

    def test_logs_uploaded_aws(self):
        pass


if __name__ == '__main__':
    if len(argv) == 2:
        TestBucketTensorboardCallback.bucket_uri = argv.pop()

        # Simple model for testing
        TestBucketTensorboardCallback.model = Sequential([
            Dense(10, activation='relu', input_shape=(10,)),
            Dense(10, activation='relu'),
            Dense(1, activation='sigmoid'),
        ])

        # The data we generate for testing
        dataset_size = 100
        TestBucketTensorboardCallback.X = rand(dataset_size, 10) * 10
        TestBucketTensorboardCallback.Y = randint(2, size=dataset_size)

        # Begin testing
        unittest.main()
    else:
        print('Usage: python test_bucket_tensorboard_callback.py bucket_uri')
        exit()
