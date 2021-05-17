from aws_cdk import (
    aws_lambda as _lambda,
    aws_lambda_python as _lambda_python,
    aws_apigatewayv2 as apigw,
    aws_apigatewayv2_integrations as apigw_int,
    aws_dynamodb as ddb,
    aws_logs as log,
    core
)

class ListBluePrints(core.Construct):

    def __init__(self, scope: core.Construct, id: str, api: apigw.HttpApi, table: ddb.Table, **kwargs):
        super().__init__(scope, id, **kwargs)

        listBluePrints = _lambda_python.PythonFunction(
            self, 'listBluePrints',
            entry='lambda/listBluePrints',
            index='listBluePrints.py',
            runtime=_lambda.Runtime.PYTHON_3_8, 
            environment={
                'TABLE_NAME': table.table_name
            },
            log_retention=log.RetentionDays.ONE_DAY,
            tracing=_lambda.Tracing.ACTIVE
        )

        table.grant_read_data(listBluePrints)

        listBluePrintsInt = apigw_int.LambdaProxyIntegration(
            handler=listBluePrints
        )

        api.add_routes(
            path='/user/blueprints',
            methods=[apigw.HttpMethod.GET],
            integration=listBluePrintsInt
        )