from PerFinDashboardLambda.models.base_model import BaseModel
class TagTransactionsTableModel(BaseModel):
    TABLE_NAME = 'TagTransactionsTable'
    def __init__(self,object=None):
        self.fields = [
            'tagId',
            'txnTimestamp',
            'internalTxnId'
        ]
        BaseModel.__init__(self,object)

