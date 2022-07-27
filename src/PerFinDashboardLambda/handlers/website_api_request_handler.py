
from PerFinDashboardLambda.models.api.website_api_request_model import WebsiteAPIRequestModel
from PerFinDashboardLambda.models.api.website_api_response_model import WebsiteAPIResponseModel
from PerFinDashboardLambda.constants import APIErrors
from PerFinDashboardLambda.processors.website_api_request_processors.attach_tag_accounts_processor import AttachTagAccountsProcessor
from PerFinDashboardLambda.processors.website_api_request_processors.create_transactions_processor import CreateTransactionsProcessor
import traceback

__api_processor_map = {
     'update_tag' : AttachTagAccountsProcessor,
     'create_transactions' : CreateTransactionsProcessor,
}

'''
Handler handles all the api calls. We would directly invoke the lambda now and later will move the lambda to a private API
'''
def WebsiteAPIRequestHandler(event,context):
     apiRequest = WebsiteAPIRequestModel(event)
     if apiRequest.Getapi() not in __api_processor_map:
          return ~ WebsiteAPIResponseModel()  \
                         .error(APIErrors.APINFOUND) \
                         .data(None)
     try:
          _api_processor = __api_processor_map[apiRequest.Getapi()](apiRequest)
          if not _api_processor.request.verify():
               return  ~ WebsiteAPIResponseModel() \
               .error(APIErrors.REQUESTERROR) \
               .data(None)
          error,data = __api_processor_map[apiRequest.Getapi()](apiRequest).callApi()
          return ~ WebsiteAPIResponseModel() \
               .error(error) \
               .data(data)
     except Exception as e:
          print(e)
          traceback.print_exc()
          return ~ WebsiteAPIResponseModel() \
               .error(APIErrors.INTERROR) \
               .data(None)







