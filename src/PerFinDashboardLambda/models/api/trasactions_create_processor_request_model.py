from PerFinDashboardLambda.models.api.api_request_model import APIRequestModel
from PerFinDashboardLambda.utils.field_verify import FieldVerify
class TransactionsCreateProcessorRequestModel(APIRequestModel):
    TRANSACTIONS_LIMIT = 10
    class TransactionCreateProcessorRequestModel(APIRequestModel):
         def __init__(self,object=None):
            self.fields = [
                'externalTxnId',
                'fromAccount',
                'toAccount',
                'txnTime',
                'txnAmount',
                'txnDescription',
                'txnType'
            ]
            self.field_validations = {
                'externalTxnId' : FieldVerify.isNonEmptyString,
                'fromAccount' : FieldVerify.isNonEmptyString,
                'toAccount' : FieldVerify.isNonEmptyString,
                'txnDescription' : FieldVerify.isNonEmptyString,
                'txnType' : FieldVerify.isNonEmptyString,
                'txnTime' : FieldVerify.isTimestampInMillis,
                'txnAmount' : FieldVerify.isAmount,
            }
            APIRequestModel.__init__(self,object)



    def __init__(self,object=None):
        self.fields = [
            'transactions'
        ]
        self.field_validations = {
            'transactions' : FieldVerify.isNonEmptyList
        }

        APIRequestModel.__init__(self,object)
        self.transactionList = {}

        #Making sure all the params are present
        if self.verify():
            #Enforcing a limit on number of transactions
            for transaction in self._transactions[:TransactionsCreateProcessorRequestModel.TRANSACTIONS_LIMIT]:
                transaction = TransactionsCreateProcessorRequestModel \
                                        .TransactionCreateProcessorRequestModel(transaction)
                if transaction.verify():
                    accountId = transaction.GetfromAccount().strip()
                    externalId = transaction.GetexternalTxnId().strip()
                    if accountId not in self.transactionList:
                        self.transactionList[accountId] = {}
                    self.transactionList[accountId][externalId] = transaction
    
                
    def getTransactions(self):
        return self.transactionList



