import boto3, json

#Check if the resource is NLB, if so skip rule evaluation
def is_nlb(nlb_arn):
    if nlb_arn.split(":")[5].split("/")[1] == "net":
        return True
    else:
        return False

# if it is an ALB, check if there is a WebACL in WAF associated with this reource
def is_waf_enabled_for_alb(elb_arn):
    webacl_id = []
    waf_regional = boto3.client('waf-regional')
    list_webacl = waf_regional.list_web_acls()

    for x in list_webacl['WebACLs']:
        webacl_id.append(x['WebACLId'])

    for x in webacl_id:
        resource_webacl = waf_regional.list_resources_for_web_acl(
            WebACLId = x,
            ResourceType = 'APPLICATION_LOAD_BALANCER'
        )
        if elb_arn in resource_webacl['ResourceArns']:
            return True

    return False

#Dpendending the status evalaution return compliant, non-compliant or NA
def evaluate_compliance(config_item, r_arn):
    if (config_item['resourceType'] != 'AWS::ElasticLoadBalancingV2::LoadBalancer'):
        return 'NOT_APPLICABLE'
    elif is_nlb(r_arn):
        return 'NOT_APPLICABLE'
    elif is_waf_enabled_for_alb(r_arn):
        return 'COMPLIANT'
    else:
        return 'NON_COMPLIANT'


# Custom AWS Config Rule - Blueprint Code
def lambda_handler(event, context):
    # Create AWS SDK clients & initialize custom rule parameters
    config = boto3.client('config')
    invoking_event = json.loads(event['invokingEvent'])
    compliance_value = 'NOT_APPLICABLE'
    resource_arn = invoking_event['configurationItem']['ARN']
    resource_id = invoking_event['configurationItem']['resourceId']

    compliance_value = evaluate_compliance(invoking_event['configurationItem'], resource_arn)

    response = config.put_evaluations(
        Evaluations=[
            {
                'ComplianceResourceType': invoking_event['configurationItem']['resourceType'],
                'ComplianceResourceId': resource_id,
                'ComplianceType': compliance_value,
                'Annotation': 'Insert text here to detail why control passed/failed',
                'OrderingTimestamp': invoking_event['notificationCreationTime']
            },
        ],
        ResultToken=event['resultToken'])
