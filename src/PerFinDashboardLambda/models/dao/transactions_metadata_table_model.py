from PerFinDashboardLambda.models.base_model import BaseModel
class TransactionsMetadataTableModel(BaseModel):
    TABLE_NAME = 'TransactionsMetadataTable'
    def __init__(self,object=None):
        self.fields = [
            'internalTxnId',
            'txnTimestamp',
            'externalTxnId',
            'accountId',
            'externalAccountId',
            'txnDescription',
            'txnAmount',
            'txnType'
        ]
        BaseModel.__init__(self,object)

