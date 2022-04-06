from PerFinDashboardLambda.models.base_model import BaseModel
class AccountingEntryTableModel(BaseModel):
    TABLE_NAME = 'AccountEntryTable'
    def __init__(self,object=None):
        self.fields = [
            'internalTxnId',
            'txnTimestamp',
            'accountId',
            'externalTxnId',
            'externalAccountId',
            'txnType',
            'txnDescription',
            'amount',
            'lastModifiedTimestamp'
        ]
        BaseModel.__init__(self,object)

