from setuptools import setup

setup(
    name='keras_clinical',
    version='1.0',
    packages=['keras_clinical'],
    license='MIT',
    long_description=open('README.md').read(),
    author='Ben Neely',
    author_email='nigelneely@gmail.com',
    description='Keras Implemented Clinical Model Zoo.',
    install_requires=[
        'tensorflow==1.4.1',
        'Keras==2.1.2'
    ]
)