from PerFinDashboardLambda.models.base_model import BaseModel
class ResourceRelationMetadataTableModel(BaseModel):
    TABLE_NAME = 'Resources_RelationsMetadataTable'
    def __init__(self,object=None):
        self.fields = [
            'resourceId',
            'ResourceGroup',
            'ResourceType',
            'ResourceValue'
        ]
        BaseModel.__init__(self,object)

