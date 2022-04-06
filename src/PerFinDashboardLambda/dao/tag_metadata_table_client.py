from PerFinDashboardLambda.dao.base_table_client import BaseTableClient
from PerFinDashboardLambda.utils.rule_engine import RuleEngine
from PerFinDashboardLambda.models.dao.tag_metadata_table_model import TagMetadataTableModel
from PerFinDashboardLambda.models.ddb.ddb_query_items_request_model import DDBQueryItemsRequestModel
# from PerFinDashboardLambda.models.dao.accounting_entry_table_model import AccountingEntryTableModel
from boto3.dynamodb.conditions import Key

class TagMetadataTableClient(BaseTableClient):
    GSI_AccountID_Status = 'accountId-status-index'
    def __init__(self):
        BaseTableClient.__init__(self,TagMetadataTableModel)

    def get_active_tags_for_account(self,accountId):
        items,lastKey = self.query_items(
            DDBQueryItemsRequestModel()
            .IndexName(TagMetadataTableClient.GSI_AccountID_Status)
            .KeyConditionExpression(Key('accountId').eq(accountId) &
                                    Key('status').eq('Active'))
        )
        return items



