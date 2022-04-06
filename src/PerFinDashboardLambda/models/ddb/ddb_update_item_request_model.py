from PerFinDashboardLambda.models.base_model import BaseModel
class DDBUpdateItemRequestModel(BaseModel):
    def __init__(self):
        self.fields = [
            'Key',
            'UpdateExpression',
            'ExpressionAttributeNames',
            'ExpressionAttributeValues'
        ]
        BaseModel.__init__(self)
