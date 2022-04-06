from PerFinDashboardLambda.models.base_model import BaseModel
class DDBBatchWriteItemsRequestModel(BaseModel):
    def __init__(self):
        self.fields = [
            'RequestItems'
        ]
        BaseModel.__init__(self)
