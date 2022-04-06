from PerFinDashboardLambda.dao.base_table_client import BaseTableClient
from PerFinDashboardLambda.models.dao.accounting_entry_table_model import AccountingEntryTableModel
from PerFinDashboardLambda.models.ddb.ddb_query_items_request_model import DDBQueryItemsRequestModel
from boto3.dynamodb.conditions import Key

class AccountingEntryTableClient(BaseTableClient):
    GSI_ExtTxnID_Timestamp = 'externalTxnId-txnTimestamp-index'
    def __init__(self):
        BaseTableClient.__init__(self,AccountingEntryTableModel)

    def put_accounting_entry(self,accountingEntry):
        return self.add_item(accountingEntry)

    def is_uniq_transaction(self,externalTxnId,txnTimestamp):
        items,lastKey = self.query_items(
            DDBQueryItemsRequestModel()
            .IndexName(AccountingEntryTableClient.GSI_ExtTxnID_Timestamp)
            .KeyConditionExpression(Key('externalTxnId').eq(externalTxnId) &
                                    Key('txnTimestamp').eq(txnTimestamp))
        )
        if len(items) > 0:
            return False
        return True


