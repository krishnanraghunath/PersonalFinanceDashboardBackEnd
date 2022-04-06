from PerFinDashboardLambda.processors.account_entry_backfill_processors.bank_statement_backfill_processor import BankStatementBackfillProcessor
import traceback
import boto3

#Mapping folders to statement processors
account_identifier_processor_map = {
     'HDFC_9096' : BankStatementBackfillProcessor,
}
#Mapping folders to account ids
account_identifier_account_id_map = {
     'HDFC_9096' : 'HDFC50100201359096'
}


def AccountEntryBackFillHandler(event,context):
     s3Client = boto3.client('s3')
     for record in event['Records']:
          fileName = record['s3']['object']['key']
          bucketName = record['s3']['bucket']['name']
          data = s3Client.get_object(Bucket=bucketName,Key=fileName)
          contents = data['Body'].read().decode("utf-8")
          accountIdentifier = fileName.split('/')[0]
          try:
               account_identifier_processor_map[accountIdentifier]().execute(
                         contents,
                          account_identifier_account_id_map[accountIdentifier]
               )

          except Exception as e:
               traceback.print_exc()
               print("Exception occured while processing Key:%s"%fileName)
