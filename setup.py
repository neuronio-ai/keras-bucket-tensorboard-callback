import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='keras-bucket-tensorboard-callback',
    version='1.0.4',
    author='Adriano Dennanni',
    author_email='adriano.dennanni@gmail.com',
    description='A Keras Callback that uploads your Tensorboard logs to a Cloud Bucket',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/neuronio-ai/keras-bucket-tensorboard-callback',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[
        'google-cloud-storage',
        'Keras',
    ],
    py_modules=['keras_bucket_tensorboard_callback'],
)
