from PerFinDashboardLambda.dao.base_table_client import BaseTableClient
from PerFinDashboardLambda.models.dao.tag_transactions_table_model import TagTransactionsTableModel

class TagTransactionsTableClient(BaseTableClient):
    GSI_AccountID_Status = 'internalTxnId-txnTimestamp-index'
    def __init__(self):
        BaseTableClient.__init__(self,TagTransactionsTableModel)

    def add_tag_txn_entry(self,tagId,accountEntry):
        self.add_item(
        TagTransactionsTableModel()
            .tagId(tagId)
            .internalTxnId(accountEntry.GetinternalTxnId())
            .txnTimestamp(accountEntry.GettxnTimestamp()))



