from PerFinDashboardLambda.models.base_model import BaseModel
class DDBWriteItemRequestModel(BaseModel):
    def __init__(self):
        self.fields = [
            'Item'
        ]
        BaseModel.__init__(self)
