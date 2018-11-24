#!/user/bin/env python

from setuptools import setup, find_packages

setup(
    name='Cloud-Fail2Ban',
    version='0.1.0',
    author='Bryan Wyatt',
    author_email='brwyatt@gmail.com',
    description=('AWS Lambda-based Fail2Ban implementation using CloudWatch, '
                 'DynamoDB, and SNS'),
    license='GPLv3',
    keywords='Fail2Ban lambda aws cloudwatch dynamo dynamodb sns sqs',
    url='https://github.com/brwyatt/Cloud-Fail2Ban',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    include_package_data=False,
    entry_points={
        'console_scripts': [
            'cloud_f2b_client = cloud_f2b.client:main',
        ],
    },
    setup_requires=[
        'pytest-runner==3.0.1',
        'setuptools==20.7.0'
    ],
    install_requires=[
        'boto3==1.7.35'
    ],
    tests_require=[
        'pytest==3.4.1',
        'pytest-cov==2.5.1'
    ]
)
