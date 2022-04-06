from PerFinDashboardLambda.models.base_model import BaseModel
class DDBQueryItemsRequestModel(BaseModel):
    def __init__(self):
        self.fields = [
            'IndexName',
            'KeyConditionExpression',
            'Limit',
            'ExpressionAttributeNames',
            'ExpressionAttributeValues',
            'ProjectionExpression',
            'ScanIndexForward',
            'FilterExpression',
            'ExclusiveStartKey'
        ]
        BaseModel.__init__(self)
