import json
from ruamel.yaml import YAML
import os
import boto3

CONFIG_FILE_NAME = 'local_envs.json'
STACK_NAME = 'Sammy-local'

def get_tables_physical_names():
    cloud_table_names = dict()

    cfn = boto3.client('cloudformation')
    stack = cfn.describe_stack_resources(StackName=STACK_NAME)

    resources = stack['StackResources']

    for resource in resources:
        if resource['ResourceType'] != 'AWS::DynamoDB::Table':
            continue
    
        resource_name = resource['LogicalResourceId']
        resource_instance_name = resource['PhysicalResourceId']

        cloud_table_names[resource_name] = resource_instance_name

    return cloud_table_names


def get_lambdas_using_dynamo_tables(table_names):
    yaml = YAML()
    template_file = open('template.yaml', 'r')
    template_data = yaml.load(template_file.read())

    lambda_dynamodb_tables = dict()

    resources = template_data['Resources']
    for resource_name in resources:
        resource = resources[resource_name]
        if resource['Type'] != 'AWS::Serverless::Function':
            continue

        env_vars = resource['Properties']['Environment']['Variables']
        lambda_dynamodb_tables[resource_name] = dict()
        for variable_name in env_vars:
            value = str(env_vars[variable_name])
            if value in table_names:
                lambda_dynamodb_tables[resource_name][value] = variable_name
    
    return lambda_dynamodb_tables


def build_json(lambdas_using_dynamo_tables, physical_table_names):
    data = {}
    for lambda_resource, table_maps in lambdas_using_dynamo_tables.items():
        lambda_overrides = {}
        for table_name, variable in table_maps.items():
            lambda_overrides[variable] = physical_table_names[table_name]

        data[lambda_resource] = lambda_overrides

    json_data = json.dumps(data);

    return json_data


logical_to_physical_table_names = get_tables_physical_names()
lambda_dynamo_tables = get_lambdas_using_dynamo_tables(logical_to_physical_table_names.keys())
config_json = build_json(lambda_dynamo_tables, logical_to_physical_table_names)

json_file = open('./config/' + CONFIG_FILE_NAME, 'w')
json_file.write(config_json)
json_file.close()
