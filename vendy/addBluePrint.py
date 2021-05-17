from aws_cdk import (
    aws_lambda as _lambda,
    aws_lambda_python as _lambda_python,
    aws_apigatewayv2 as apigw,
    aws_apigatewayv2_integrations as apigw_int,
    aws_dynamodb as ddb,
    aws_logs as log,
    core
)

class AddBluePrint(core.Construct):

    def __init__(self, scope: core.Construct, id: str, api: apigw.HttpApi, table: ddb.Table, **kwargs):
        super().__init__(scope, id, **kwargs)

        addBluePrint = _lambda_python.PythonFunction(
            self, 'addBluePrint',
            entry='lambda/addBluePrint',
            index='addBluePrint.py',
            runtime=_lambda.Runtime.PYTHON_3_8, 
            environment={
                'TABLE_NAME': table.table_name
            },
            log_retention=log.RetentionDays.ONE_DAY,
            tracing=_lambda.Tracing.ACTIVE,
        )

        table.grant_read_write_data(addBluePrint)

        updateBluePrintInt = apigw_int.LambdaProxyIntegration(
            handler=addBluePrint
        )

        api.add_routes(
            path='/admin/blueprint',
            methods=[apigw.HttpMethod.POST],
            integration=updateBluePrintInt
        )