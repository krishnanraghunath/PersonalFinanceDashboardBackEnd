from PerFinDashboardLambda.dao.tag_metadata_table_client import TagMetadataTableClient
from PerFinDashboardLambda.dao.resource_metadata_table_client import ResourceRelationMetadataTableClient
from PerFinDashboardLambda.dao.tag_transactions_table_client import TagTransactionsTableClient
from PerFinDashboardLambda.dao.transactions_metadata_table_client import TransactionsMetadataTableModel
from PerFinDashboardLambda.utils.rule_engine import RuleEngine

class TagRulesProcessor:
    def __init__(self):
        self.tagMetadatTableClient = TagMetadataTableClient()
        self.tagTransactionsTableClient = TagTransactionsTableClient()
        self.resourceMetadataTableClient = ResourceRelationMetadataTableClient()
        self.account_tags = {}
        self.tag_rules = {}

    def get_tag_rule(self,tagId):
        if tagId not in self.tag_rules:
            self.tag_rules[tagId] =  RuleEngine(self.tagMetadatTableClient.get_tag_rules_for_tagId(tagId))
        return self.tag_rules[tagId]

    def get_tag_ids_for_accountId(self,accountId):
        if accountId not in self.account_tags:
            self.account_tags[accountId] = list(map(lambda y:y.GetResourceGroup(),
                        self.resourceMetadataTableClient.get_resource_groups(accountId,'ATTACHED_ACCOUNT')))
        return self.account_tags[accountId]
    

    def process_entry(self,transactionEntry):
        accountId = transactionEntry['accountId']
        for tagId in self.get_tag_ids_for_accountId(accountId):
            if self.get_tag_rule(tagId).match(transactionEntry):
                self.tagTransactionsTableClient.add_tag_txn_entry(
                                                tagId,
                                                TransactionsMetadataTableModel().ingest(transactionEntry))


        

        