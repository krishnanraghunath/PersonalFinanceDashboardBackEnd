from PerFinDashboardLambda.dao.tag_metadata_table_client import TagMetadataTableClient
from PerFinDashboardLambda.dao.tag_transactions_table_client import TagTransactionsTableClient
from PerFinDashboardLambda.models.dao.accounting_entry_table_model import AccountingEntryTableModel
from PerFinDashboardLambda.utils.rule_engine import RuleEngine

def TagRulesMatcherHandler(event,context):
     tagMetadatTableClient = TagMetadataTableClient()
     tagTransactionsTableClient = TagTransactionsTableClient()
     accountId_tagRules = {}
     for record in event['Records']:
          print(record)
          if record['eventName'] in ['INSERT','MODIFY']:
               new_image = record['dynamodb']['NewImage']
               for key in new_image:
                    try:
                         new_image[key] = new_image[key]['S']
                    except:
                         new_image[key] = int(new_image[key]['N'])
               accountId = new_image['accountId']
               if accountId not in accountId_tagRules:
                    accountId_tagRules[accountId] =tagMetadatTableClient.get_active_tags_for_account(accountId)

               for accountId_tagRule in accountId_tagRules[accountId]:
                    ruleEngine = RuleEngine(accountId_tagRule.GettagRules())
                    if ruleEngine.match(new_image):
                         tagTransactionsTableClient.add_tag_txn_entry(
                                                       accountId_tagRule,
                                                       AccountingEntryTableModel().ingest(new_image))

     tagTransactionsTableClient.batch_write_items(True)




