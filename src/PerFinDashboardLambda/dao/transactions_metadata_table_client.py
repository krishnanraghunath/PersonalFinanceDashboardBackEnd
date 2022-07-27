from PerFinDashboardLambda.dao.base_table_client import BaseTableClient
from PerFinDashboardLambda.utils.common_utils import CommonUtils
from PerFinDashboardLambda.models.dao.transactions_metadata_table_model import TransactionsMetadataTableModel


class TransactionsMetadataTableClient(BaseTableClient):
    def __init__(self):
        BaseTableClient.__init__(self,TransactionsMetadataTableModel)

    def add_transaction(self,fromAccount,toAccount,externalTxnId,txnType,txnAmount,txnDescription,txnTimestamp):
        internalTxnId = CommonUtils.MD5(fromAccount.strip() + externalTxnId.strip())
        if txnType not in ['DEBIT','CREDIT']:
            return False
        return self.add_item(
            TransactionsMetadataTableModel()
                .internalTxnId(internalTxnId)
                .txnTimestamp(txnTimestamp)
                .accountId(fromAccount.strip())
                .externalAccountId(toAccount.strip())
                .externalTxnId(externalTxnId.strip())
                .txnDescription(txnDescription)
                .txnType(txnType)
                .txnAmount(txnAmount))
           
