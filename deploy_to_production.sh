#!/bin/bash
STACK_NAME=PersonalFinanceBackEndStack
BUCKET_NAME=personalfinancebackendstackartifacts
echo '#######################Creating Bucket '$BUCKET_NAME'################'
aws s3 mb s3://$BUCKET_NAME
echo '#######################Creating Python Layer '
cd lib
rm -rf python 
docker pull lambci/lambda:build-python3.6
docker run --rm -v `pwd`:/var/task lambci/lambda:build-python3.6 pip install pdfminer==20191125 -t python 
cd ..
echo '#######################Building '
aws cloudformation package --template-file template.yaml --s3-bucket $BUCKET_NAME --output-template-file out.yml
aws cloudformation deploy --template-file out.yml --stack-name $STACK_NAME --capabilities CAPABILITY_NAMED_IAM
