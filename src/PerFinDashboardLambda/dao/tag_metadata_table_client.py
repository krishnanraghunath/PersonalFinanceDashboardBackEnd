from PerFinDashboardLambda.dao.base_table_client import BaseTableClient
from PerFinDashboardLambda.utils.rule_engine import RuleEngine
from PerFinDashboardLambda.models.dao.tag_metadata_table_model import TagMetadataTableModel
from PerFinDashboardLambda.models.ddb.ddb_get_item_request_model import DDBGetItemRequestModel

class TagMetadataTableClient(BaseTableClient):
    def __init__(self):
        BaseTableClient.__init__(self,TagMetadataTableModel)

    def get_tag_rules_for_tagId(self,tagId):
        resp,item = self.get_item(DDBGetItemRequestModel().Key({'tagId':tagId}))
        try:
            if item.Getstatus() == 'ACTIVE':
                return item.GettagRules()
            return {}
        except:
            return {}
    
        



