from PerFinDashboardLambda.dao.resource_metadata_table_client import ResourceRelationMetadataTableClient
from PerFinDashboardLambda.dao.transactions_metadata_table_client import TransactionsMetadataTableClient
from PerFinDashboardLambda.processors.website_api_request_processors.basic_request_processor import BasicRequestProcessor
from PerFinDashboardLambda.models.api.trasactions_create_processor_request_model import TransactionsCreateProcessorRequestModel
from PerFinDashboardLambda.utils.common_utils import CommonUtils
from decimal import Decimal

class CreateTransactionsProcessor(BasicRequestProcessor):
    def __init__(self,event):
        self.resourceMetadataTableClient = ResourceRelationMetadataTableClient()
        self.transactionsTableClient = TransactionsMetadataTableClient()
        BasicRequestProcessor.__init__(self,event,TransactionsCreateProcessorRequestModel)


    def callApi(self):
        current_resources_accounts = list(map(lambda x:x.GetResourceValue(),self.resourceMetadataTableClient\
                                                .get_resource_values(self.input.Getuser_id(),
                                                                                'ACCOUNT')))
        transactions = self.request.getTransactions()
        for accountId in transactions:
            if accountId not in current_resources_accounts:
                continue
            for externalId in transactions[accountId]:
                transaction = transactions[accountId][externalId]
                self.transactionsTableClient.add_transaction(
                    transaction.GetfromAccount().strip(),
                    transaction.GettoAccount().strip(),
                    externalId.strip(),
                    transaction.GettxnType().strip(),
                    CommonUtils.amount(transaction.GettxnAmount()),
                    transaction.GettxnDescription().strip(),
                    int(transaction.GettxnTime())
                )
        self.transactionsTableClient.batch_write_items(force = True)
        return None,{}
