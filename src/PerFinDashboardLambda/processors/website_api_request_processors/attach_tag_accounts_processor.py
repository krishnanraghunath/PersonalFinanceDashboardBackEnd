from PerFinDashboardLambda.dao.resource_metadata_table_client import ResourceRelationMetadataTableClient
from PerFinDashboardLambda.processors.website_api_request_processors.basic_request_processor import BasicRequestProcessor
from PerFinDashboardLambda.models.api.attach_tag_account_processor_request_model import AttachTagAccountProcessorRequestModel
from PerFinDashboardLambda.utils.common_utils import CommonUtils
from PerFinDashboardLambda.models.dao.resource_relation_metadata_table_model import ResourceRelationMetadataTableModel

class AttachTagAccountsProcessor(BasicRequestProcessor):
    def __init__(self,event):
        self.resourceMetadataTableClient = ResourceRelationMetadataTableClient()
        BasicRequestProcessor.__init__(self,event,AttachTagAccountProcessorRequestModel)

    def callApi(self):
        tagId = CommonUtils.MD5(self.input.Getuser_id() + self.request.GettagName())
        current_resources_attached = self.resourceMetadataTableClient\
                                                .get_resource_values(tagId,'ATTACHED_ACCOUNT')
        current_resources_accounts = self.resourceMetadataTableClient\
                                                .get_resource_values(self.input.Getuser_id(),
                                                                                'ACCOUNT')
        user_accounts = list(map(lambda y:y.GetResourceValue(),current_resources_accounts))
        current_items = list(map(lambda y:y.GetResourceValue(),current_resources_attached))
        accountsToAttach = list(filter(lambda y:y in user_accounts,self.request.Getaccounts()))

        items_to_add = list(filter(lambda y:y not in current_items,accountsToAttach))
        items_to_remove = list(filter(lambda y:y not in accountsToAttach,current_items))
        itemids_to_remove = list(map(lambda y:y.GetresourceId(), \
                                    list(filter(lambda x:x.GetResourceValue() in items_to_remove, \
                                           current_resources_attached ))))
        self.resourceMetadataTableClient.remove_resource_values(itemids_to_remove)
        resource_to_add = [ResourceRelationMetadataTableModel()   
                                            .ResourceGroup(tagId)
                                            .ResourceType('ATTACHED_ACCOUNT')
                                            .ResourceValue(item) for item in items_to_add]
        self.resourceMetadataTableClient.add_resource_values(resource_to_add)
        return None,{}
        


