# govern8r

This is the repo for the govern8r setup script.

## Environment setup

Unfortunately, for right now we need to use python 2.7.11.

Install virtualenv for both client and server. 
```
virtualenv -p <path-to-python-2.7.11> govern8rClient
virtualenv -p <path-to-python-2.7.11> govern8rService
virtualenv -p <path-to-python-2.7.11> govern8rLib
```

## Access

ALWAYS USE A NON-ROOT USER FOR ACCESSING AWS.

## Elastic beanstalk

There is some policy that needs to be created

This is the user policy: BeanstalkUserPolicy
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "iam:PassRole",
                "iam:AttachRolePolicy",
                "iam:ListRolePolicies",
                "iam:ListPolicies",
                "iam:ListAttachedRolePolicies",
                "iam:ListInstanceProfilesForRole",
                "iam:ListInstanceProfiles",
                "iam:AddRoleToInstanceProfile",
                "iam:CreateInstanceProfile",
                "iam:CreateRole",
                "iam:CreatePolicy",
                "iam:ListRoles",
                "kinesis:*",
                "kms:*",
                "appstream:*",
                "elasticache:*",
		        "elasticbeanstalk:*",
		        "ec2:*",
		        "elasticmapreduce:*",
		        "elasticloadbalancing:*",
		        "autoscaling:*",
		        "cloudwatch:*",
		        "s3:*",
		        "sns:*",
		        "cloudformation:*",
		        "rds:*",
		        "sqs:*",
		        "dynamodb:*",
		        "cloudhsm:*",
		        "machinelearning:*",
		        "datapipeline:*",
		        "glacier:*",
		        "firehose:*",
		        "elastictranscoder:*",
		        "es:*",
		        "sns:*",
		        "ssm:*",
		        "lambda:*",
		        "sdb:*",
		        "codecommit:*",
		        "codedeploy:*",
		        "redshift:*",
		        "sqs:*",
		        "codepipeline:*",
		        "apigateway:*"
            ],
            "Resource": "*"
        }
    ]
}

This is the service policy: BeanstalkServicePolicy
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "elasticloadbalancing:DescribeInstanceHealth",
                "ec2:DescribeInstances",
                "ec2:DescribeInstanceStatus",
                "ec2:GetConsoleOutput",
                "ec2:AssociateAddress",
                "ec2:DescribeAddresses",
                "ec2:DescribeSecurityGroups",
                "sqs:GetQueueAttributes",
                "sqs:GetQueueUrl",
                "autoscaling:DescribeAutoScalingGroups",
                "autoscaling:DescribeAutoScalingInstances",
                "autoscaling:DescribeScalingActivities",
                "autoscaling:DescribeNotificationConfigurations",
               	"iam:PassRole"
            ],
            "Resource": [
                "*"
            ]
        }
    ]
}



There are some roles that need to be created:

```
aws-elasticbeanstalk-ec2-role
aws-elasticbeanstalk-service-role
```

Attach to each of these roles the following policies:

```
AWSCloudHSMRole
AmazonS3FullAccess
AmazonAPIGatewayInvokeFullAccess
AWSCloudHSMFullAccess
AmazonDynamoDBFullAccess
AmazonSESFullAccess
```

## Encryption Keys

We need to create an encryption key for the govern8r service. Use the following alias:

```
alias/govern8r
```

The ARN for this key will need to be placed in the govern8rService configuration file.



