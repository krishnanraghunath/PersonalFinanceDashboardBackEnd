
from PerFinDashboardLambda.dao.base_table_client import BaseTableClient
from PerFinDashboardLambda.models.ddb.ddb_get_item_request_model import DDBGetItemRequestModel
from PerFinDashboardLambda.models.dao.account_metadata_table_model import AccountMetadataTableModel

class AccountMetadataTableClient(BaseTableClient):
    def __init__(self):
        BaseTableClient.__init__(self,AccountMetadataTableModel)

    def get_account_details_for_account_id(self,accountId):
        resp,item = self.get_item(DDBGetItemRequestModel().Key({'accountId':accountId}))
        try:
            if item.Getstatus() == 'ACTIVE':
                return item
            return None
        except:
            return None
