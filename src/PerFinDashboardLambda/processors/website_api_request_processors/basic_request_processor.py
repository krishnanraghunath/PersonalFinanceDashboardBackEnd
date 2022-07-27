
class BasicRequestProcessor:
    def __init__(self,event,requestModel):
        self.input = event
        self.request = requestModel(self.input.Getparams())
    
    def callApi(self):
        return 'NOT DEFINED',None

