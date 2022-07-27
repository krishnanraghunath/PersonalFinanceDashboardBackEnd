from PerFinDashboardLambda.dao.base_table_client import BaseTableClient
from PerFinDashboardLambda.models.dao.resource_relation_metadata_table_model import ResourceRelationMetadataTableModel
from PerFinDashboardLambda.models.ddb.ddb_query_items_request_model import DDBQueryItemsRequestModel
from PerFinDashboardLambda.models.ddb.ddb_delete_item_request_model import DDBDeleteItemRequestModel
from PerFinDashboardLambda.utils.common_utils import CommonUtils
from boto3.dynamodb.conditions import Key


class ResourceRelationMetadataTableClient(BaseTableClient):
    RESOURCEGROUPTYPEINDEX = 'ResourceGroup-ResourceType-index'
    RESOURCEVALUETYPEINDEX = 'ResourceValue-ResourceType-index'
    def __init__(self):
        BaseTableClient.__init__(self,ResourceRelationMetadataTableModel)

    def get_resource_values(self,resourceGroup,resourceType):
        items = self.query_all(
            DDBQueryItemsRequestModel()
            .IndexName(ResourceRelationMetadataTableClient.RESOURCEGROUPTYPEINDEX)
            .KeyConditionExpression(Key('ResourceGroup').eq(resourceGroup) &
                                    Key('ResourceType').eq(resourceType))
        )
        return items

    
    def get_resource_groups(self,resoureValue,resourceType):
        items = self.query_all(
            DDBQueryItemsRequestModel()
            .IndexName(ResourceRelationMetadataTableClient.RESOURCEVALUETYPEINDEX)
            .KeyConditionExpression(Key('ResourceValue').eq(resoureValue) &
                                    Key('ResourceType').eq(resourceType))
        )
        return items

    def remove_resource_values(self,resourceIds):
        for resourceId in resourceIds:
            self.add_delete_item(DDBDeleteItemRequestModel() 
                                    .Key(~ResourceRelationMetadataTableModel()  
                                            .resourceId(resourceId)))
        self.batch_write_items(force=True)


    def add_resource_values(self,resources):
        for resource in resources:
            self.add_item(resource.resourceId(CommonUtils.MD5( 
               resource.GetResourceGroup() +   
                resource.GetResourceType() +  
                resource.GetResourceValue() 
            )))
        self.batch_write_items(force=True)

        




