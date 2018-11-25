# Cloud Fail2Ban
Fail2Ban implementation to parse logs streamed from CloudWatch in Lambda, and push bans to SNS topics

## Development

### Dev Setup

Preparing the development environment

```
pyvenv env
. env/bin/activate
pip install -e .
```

### Running unit tests

```
. env/bin/activate
python ./setup.py pytest
```

## Building

Building the Lambda package

```
bin/mk_lambda.sh
```

This will collect all necessary files for running the Lambda function and output to `build/lambda.zip`, ready to be uploaded to AWS Lambda.

## Installing/Deploying

### Additional resources

Various additional AWS rsources are used to make this system work.

#### CloudWatch

CloudWatch is used to stream logs to the Lambda function (either the all-in-one, or the first phase function). This is the source of data used to match against filters.

#### Lambda

Lambda is used as the execution environment for the Lambda functions, and must have access to the DynamoDB table and SNS topic.

#### DynamoDB

DynamoDB stores records of matches against the filter set. These records are then checked against the jail rules to determine if there are enough matches in a given time for a given set of filters. In a 2-phase setup, DynamoDB triggers are used to execute the 2nd phase jail Lambda function.

#### SNS

An SNS topic is used as the endpoint to send ban messages to. SQS queues subscribe to this topic in order to receive ban notifications.

#### SQS

Clients create SQS queues and subscribe them to the SNS topic, using filters to control which jails they want to receive ban messages for.

#### Client Code

The client code (`cloud_f2b.client`) is configured as an entry point in the repository's `setup.py`. This module may be installed on hosts with access to create SQS queues and subsccribe to the SNS topic to receive ban notifications. The user running the code must have `sudo` access to run the `fail2ban-client` command and may be run as a service.

If Puppet is available, [this Puppet module](https://github.com/brwyatt/puppet-cloud_fail2ban) can be used to deploy this module to hosts into it's own Python Virtual Environment.

### Lambda Functions

There are 3 files under the `lambda` directory that can be used in two different ways:

#### Single Lambda (Single-Region)

`main.py:cloudwatch_run_filters_and_jails` provides an all-in-one Lambda function that may be used as a single-phase setup, checking jail rules immediately after checking logs for matches against the filters. This is good for single-region deployments that do not leverage DynamoDB Global Tables and DynamoDB Triggers.

#### 2-Phase Lambda (Multi-Region)

This repository contains two alternate functions that are sufficient for a multi-region architecture and leverage a 2-phase Lambda configuration.

`main.py:cloudwatch_run_filters` provides the first phase code that will accept logs streamed from CloudWatch, check the lines against the filters, and insert rows into DynamoDB.

`main.py:dynamodb_run_jails` receives row update information from DynamoDB triggers, checks the data stored in DynamoDB against jail rules for filter in the updated row(s), and sends out a ban alert to the SNS topic if the IP address is above a jail's threshold.

This allows for jail rules to be tested in all regions based on new matches from any region.
