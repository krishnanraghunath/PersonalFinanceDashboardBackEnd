from PerFinDashboardLambda.models.base_model import BaseModel
class WebsiteAPIResponseModel(BaseModel):
    def __init__(self,object=None):
        self.fields = [
            'error',
            'data'
        ]
        BaseModel.__init__(self,object)