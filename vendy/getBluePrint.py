from aws_cdk import (
    aws_lambda as _lambda,
    aws_lambda_python as _lambda_python,
    aws_apigatewayv2 as apigw,
    aws_apigatewayv2_integrations as apigw_int,
    aws_dynamodb as ddb,
    aws_logs as log,
    core
)

class GetBluePrint(core.Construct):

    def __init__(self, scope: core.Construct, id: str, api: apigw.HttpApi, table: ddb.Table, **kwargs):
        super().__init__(scope, id, **kwargs)

        getBluePrint = _lambda_python.PythonFunction(
            self, 'getBluePrint',
            entry='lambda/getBluePrint',
            index='getBluePrint.py',
            runtime=_lambda.Runtime.PYTHON_3_8, 
            environment={
                'TABLE_NAME': table.table_name
            },
            log_retention=log.RetentionDays.ONE_DAY,
            tracing=_lambda.Tracing.ACTIVE,
        )

        table.grant_read_data(getBluePrint)

        getBluePrintInt = apigw_int.LambdaProxyIntegration(
            handler=getBluePrint
        )

        api.add_routes(
            path='/user/blueprint',
            methods=[apigw.HttpMethod.GET],
            integration=getBluePrintInt
        )