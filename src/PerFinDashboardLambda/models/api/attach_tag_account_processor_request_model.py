from PerFinDashboardLambda.models.api.api_request_model import APIRequestModel
from PerFinDashboardLambda.utils.field_verify import FieldVerify
class AttachTagAccountProcessorRequestModel(APIRequestModel):
    def __init__(self,object=None):
        self.fields = [
            'tagName',
            'accounts'
        ]
        self.field_validations = {
            'tagName' : FieldVerify.isNonEmptyString,
            'accounts' : FieldVerify.isNonEmptyList
        }
        APIRequestModel.__init__(self,object)