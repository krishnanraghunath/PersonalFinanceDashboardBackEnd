from PerFinDashboardLambda.models.base_model import BaseModel
class TagMetadataTableModel(BaseModel):
    TABLE_NAME = 'TagMetadataTable'
    def __init__(self,object=None):
        self.fields = [
            'tagId',
            'acountId',
            'tagName',
            'tagColor',
            'tagRules',
            'status'
        ]
        BaseModel.__init__(self,object)

