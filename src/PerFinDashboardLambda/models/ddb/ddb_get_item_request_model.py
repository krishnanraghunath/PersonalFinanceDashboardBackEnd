from PerFinDashboardLambda.models.base_model import BaseModel
class DDBGetItemRequestModel(BaseModel):
    def __init__(self):
        self.fields = [
            'Key',
            'TableName',
            'AttributesToGet',
            'ProjectionExpression',
            'ExpressionAttributeNames'
        ]
        BaseModel.__init__(self)
