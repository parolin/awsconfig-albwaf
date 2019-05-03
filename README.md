# Introduction
AWS Config Rules enables you to implement security policies as code for your organization and evaluate configuration changes to AWS resources against these policies.

AWS provides a number of predefined, managed Config rules. You also can create custom Config rules based on criteria you define within an AWS Lambda function.

This create a custom rule that audits AWS resources for security compliance by inpecting your Application Load Balance (ALB) and validate if it has an WAF WebACL associated with the ALB. 

The custom rule helps to implement Defense in Depth ensuring you have a WAF to mitigate Layer7 attacks in your ALB.

It is also part of the [AWS Best Practices for DDoS Resiliency](https://d1.awsstatic.com/whitepapers/Security/DDoS_White_Paper.pdf "AWS Best Practices for DDoS Resiliency")

# Setup Environment

## Create IAM Role
The IAM role will be used by the Lambda function to assume role and perform the compliance evaluation in your resources.

To create the IAM role, go to the [IAM console](https://console.aws.amazon.com/iam), choose Roles in the navigation pane, click Create Role, and follow the wizard.

In the first step, select AWS Service as trusted entity, and choose Lambda as the service that will use this role.

In Permissions, attach the following permissions policies:
* AmazonEC2ReadOnlyAccess
* AWSWAFReadOnlyAccess
* AWSLambdaExecute
* AWSConfigRulesExecutionRole

In Tags page, add any Tag that you want

In the Review page, select the Role Name you want, and any description that you wish.

Click in Create Role.

## Create the Lambda function for the custom rule
To create the Lambda function that contains logic for the custom rule, go to the [Lambda console](https://console.aws.amazon.com/lambda/), click Create Function, and then choose Author from scratch.

In fucntion name, add the Lambda fcuntion name that you want. in Runtime select Python 3.7

In the Permissions section, extended it and in the Drop down list for Execution Role select Use an existing role.

In the Existing role dropdown list, select the role you create in the step above

Click in Create function button

In the function code part, remove the text added by AWS, and copy the content from lambda_blueprint.py in this repository

Click in Save (in the top right)

Above the Save button, there the Lambda function ARN. Take note of your AWS Lambda function ARN. You will need when creating the AWS Config Custom Rule

## Create a custom Config rule
The last step is to create a custom Config rule and use the Lambda function as the source. To do this, go to the [Config console](https://console.aws.amazon.com/config), choose Rules in the navigation pane, click Add rule, and then click Add custom rule.

Enter name for your custom rule, as well any description you want.

In AWS Lambda function ARN, add the ARN for your Lambda function that youc reated in the step above

In Trigger type select Configuration changes.

In Resources select LoadBalancer under  ElasticLoadBalancingV2, and WebACL under WAFRegional

Rule parameters and remediation action can kept as default.

Click in Save

## Behavior
Any ALB resources that are created or modified will now be checked against the custom AWS Config rule created for compliance.

All WebACL that are created or modified will also trigger the rule to check if your ALB is compliant or not.

From the Config console, you will be able to see if any resources do not comply with the control requirement.

# Improvements
I am working in an installer that will create the IAM role, Lambda function and the Config rule making it faster to deploy

