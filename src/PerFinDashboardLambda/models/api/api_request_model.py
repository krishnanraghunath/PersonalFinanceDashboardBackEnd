from PerFinDashboardLambda.models.base_model import BaseModel

class APIRequestModel(BaseModel):
    def __init__(self,object):
        self.field_validations = {
        }
        BaseModel.__init__(self,object)
    

    def verify(self):
        for field in self.field_validations:
           fieldValue = getattr(self,'_'+field) 
           fieldValidate = self.field_validations[field]
           if(fieldValidate(fieldValue) == False):
            return False
        return True
