from aws_cdk import(
    core as cdk,
    aws_apigatewayv2 as apigw,
    aws_dynamodb as ddb
)

from listBluePrints import ListBluePrints
from getBluePrint import GetBluePrint
from addBluePrint import AddBluePrint
from addBluePrintVersion import AddBluePrintVersion

class VendyStack(cdk.Stack):

    def __init__(self, scope: cdk.Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        table = ddb.Table(
            self, 'coreTable',
                partition_key={'name': 'blueprintName', 'type': ddb.AttributeType.STRING},
                sort_key={'name': 'version', 'type': ddb.AttributeType.STRING}
        )

        table.add_global_secondary_index(
            index_name='latest',
            partition_key={'name': 'version', 'type': ddb.AttributeType.STRING},
        )

        api = apigw.HttpApi(
            self, 'userAPI',
        )

        #listBluePrintsApi = ListBluePrints(self, 'listBluePrints', api, table)
        GetBluePrintApi = GetBluePrint(self, 'getBluePrint', api, table)
        AddBluePrintApi = AddBluePrint(self, 'addBluePrint', api, table)
        AddBluePrintVersionApi = AddBluePrintVersion(self, 'addBluePrintVersion', api, table)