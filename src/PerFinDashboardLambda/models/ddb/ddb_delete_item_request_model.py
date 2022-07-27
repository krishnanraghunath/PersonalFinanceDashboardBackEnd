from PerFinDashboardLambda.models.base_model import BaseModel
class DDBDeleteItemRequestModel(BaseModel):
    def __init__(self):
        self.fields = [
            'Key',
            'ConditionExpression',
            'ConditionalOperator',
            'ExpressionAttributeNames',
            'ExpressionAttributeValues'
        ]
        BaseModel.__init__(self)
