from PerFinDashboardLambda.models.base_model import BaseModel
class WebsiteAPIRequestModel(BaseModel):
    def __init__(self,object=None):
        self.fields = [
            'user_id',
            'api',
            'params'
        ]
        
        BaseModel.__init__(self,object)