from PerFinDashboardLambda.models.base_model import BaseModel
class TagMetadataTableModel(BaseModel):
    TABLE_NAME = 'TagMetadataTable'
    def __init__(self,object=None):
        self.fields = [
            'tagId',
            'tagRules',
            'user_id',
            'creationTime',
            'lastModifiedTime',
            'tagName',
            'status'
        ]
        BaseModel.__init__(self,object)

