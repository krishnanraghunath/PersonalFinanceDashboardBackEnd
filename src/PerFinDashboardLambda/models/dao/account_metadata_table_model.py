from PerFinDashboardLambda.models.base_model import BaseModel
class AccountMetadataTableModel(BaseModel):
    TABLE_NAME = 'AccountMetadataTable'
    def __init__(self,object=None):
        self.fields = [
            'accountId',
            'accountName',
            'accountNumber',
            'accountType',
            'creationTime',
            'institution',
            'lastModifiedTime',
            'status',
            'user_id'
        ]
        BaseModel.__init__(self,object)

