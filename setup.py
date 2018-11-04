#!/user/bin/env python

from setuptools import setup

setup(
    name='F2B_Lambda',
    version='0.1.0',
    author='Bryan Wyatt',
    author_email='brwyatt@gmail.com',
    description=('AWS Lambda-based Fail2Ban implementation using DynamoDB '
                 'and SNS'),
    license='GPLv3',
    keywords='Fail2Ban lambda aws dynamo dynamodb sns',
    url='https://github.com/brwyatt/F2B_Lambda',
    packages=['F2B'],
    package_dir={'': 'src'},
    include_package_data=False,
    setup_requires=[
        'setuptools==40.5.0',
        'pytest-runner==4.2'
    ],
    install_requires=[
        'boto3==1.7.35'
    ],
    tests_require=[
        'pytest==3.10.0',
        'pytest-cov==2.6.0'
    ]
)
