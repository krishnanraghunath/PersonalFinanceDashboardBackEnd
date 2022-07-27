from PerFinDashboardLambda.dao.account_metadata_table_client import AccountMetadataTableClient
from PerFinDashboardLambda.processors.statement_processors.basic_processor import BasicProcessor

def StatementsProcessor(event,context):
    accountMetadataTableClient = AccountMetadataTableClient()
    for record in event['Records']:
        if 'NewImage' not in record['dynamodb']:
            continue
        status = record['dynamodb']['NewImage']['status']['S']
        s3Key = record['dynamodb']['NewImage']['fileId']['S'] 
        accountId = record['dynamodb']['NewImage']['targetId']['S'] 
        fileType = record['dynamodb']['NewImage']['fileType']['S']
        if status == 'UPLOADED':
            accountDetails = accountMetadataTableClient.get_account_details_for_account_id(accountId)
            processed = BasicProcessor(s3Key).process(accountDetails,fileType)
            #TODO: Update the status in DDB for the file
        



        