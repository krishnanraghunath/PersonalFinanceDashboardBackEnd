from PerFinDashboardLambda.constants import STATEMENTS_UPLOAD_BUCKET
from PerFinDashboardLambda.processors.statement_processors._processors_map import ProcessorsMapping
from PerFinDashboardLambda.dao.transactions_metadata_table_client import TransactionsMetadataTableClient
from PerFinDashboardLambda.utils.common_utils import CommonUtils
from datetime import datetime
from time import mktime
import boto3

class BasicProcessor:
    def __init__(self,s3File):
        s3 = boto3.resource('s3')
        self.fileName = None
        self.transactionTableClient = TransactionsMetadataTableClient()
        try:
            s3.Bucket(STATEMENTS_UPLOAD_BUCKET).download_file(s3File,"/tmp/" + s3File)
            self.fileName = "/tmp/" + s3File
        except Exception as e:
            import traceback
            traceback.print_exc()
            

    def process(self,accountDetails,fileType):
        if self.fileName == None:
            print("File is not downloaded.")
            return False,None
        processorId = accountDetails.Getinstitution() + ':' + accountDetails.GetaccountType()+':'+fileType
        if processorId not in ProcessorsMapping:
            print ("No processors found for the account -> %s"%processorId)
            return False,None
        print("Processor ID => " + processorId)
        processor = ProcessorsMapping[processorId](self.fileName,accountDetails)
        if processor.initialise():
            response,transactions = processor.process()
            if response:
                for transaction in transactions:
                    date = datetime.strptime(transaction['txnTimestamp']['value']['date'],"%d/%m/%Y")
                    fromAccount = accountDetails.GetaccountNumber()
                    date_timestamp = int(mktime(date.timetuple())*1000) 
                    externalTxnId = CommonUtils.MD5(    
                                            str(fromAccount)+
                                            str(date_timestamp)+
                                            str(transaction['txnDescription']['line']))
                    self.transactionTableClient.add_transaction(
                        fromAccount,
                        'EXTERNAL',
                        externalTxnId,
                        transaction['txnAmount']['value']['txnType'],
                        transaction['txnAmount']['value']['amount'],
                        transaction['txnDescription']['value']['description'],
                        date_timestamp
                    )
                self.transactionTableClient.batch_write_items(force=True)
                return True
            else:
                print("Error happened while processing File:%s" %self.fileName)
        else:
            print("Unable to Initialise Processor")
        return False
