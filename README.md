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
