from datetime import date
from PerFinDashboardLambda.processors.statement_processors.line_processors.amount_line_processor import AmountLineProcessor
from PerFinDashboardLambda.processors.statement_processors.pdf_statement_processor import PDFStatementProcessor
from PerFinDashboardLambda.constants import HDFC_CC_STATEMENT_PROCESSOR
from decimal import Decimal
def process_card_number(line):
    return {"cardNumber":''.join(line.split('Card No:')[1].split(' '))}

class HDFCCCStatementProcessor(PDFStatementProcessor):
    HDFC_DUE_ERROR_THRESHOLD = 50
    HDFC_PAYMENTS_DEBITS_ERROR_THRESHOLD = 25
    def __init__(self,fileName,accountDetails):
        PDFStatementProcessor.__init__(self,fileName,accountDetails)
        self.statementAmountLineProcessor = AmountLineProcessor()
        self.amountLineProcessor.set_start_regexes(HDFC_CC_STATEMENT_PROCESSOR.AMOUNT_LINE_START_REGEX)
        self.amountLineProcessor.set_stop_regexes(HDFC_CC_STATEMENT_PROCESSOR.AMOUNT_LINE_STOP_REGEX)
        self.statementAmountLineProcessor.set_start_regexes(HDFC_CC_STATEMENT_PROCESSOR.STATEMENT_AMOUNT_LINE_START_REGEX)
        self.statementAmountLineProcessor.set_stop_regexes(HDFC_CC_STATEMENT_PROCESSOR.STATEMENT_AMOUNT_LINE_STOP_REGEX)
        self.descriptionLineProcessor.set_start_regexes(HDFC_CC_STATEMENT_PROCESSOR.DESCRIPTION_LINE_START_REGEX)
        self.descriptionLineProcessor.set_stop_regexes(HDFC_CC_STATEMENT_PROCESSOR.DESCRIPTION_LINE_STOP_REGEX)
        self.descriptionLineProcessor.set_no_match_regexes(HDFC_CC_STATEMENT_PROCESSOR.DESCRIPTION_LINE_NO_MATCH_REGEX)
        self.dateLineProcessor.set_stop_regexes(HDFC_CC_STATEMENT_PROCESSOR.DATE_LINE_STOP_REGEX)
        self.accountDetailsProcessor.set_start_regexes(HDFC_CC_STATEMENT_PROCESSOR.ACCOUNT_DETAILS_LINE_START_REGEX)
        self.accountDetailsProcessor.set_stop_regexes(HDFC_CC_STATEMENT_PROCESSOR.ACCOUNT_DETAILS_LINE_STOP_REGEX)
        self.accountDetailsProcessor.set_match_regexes(HDFC_CC_STATEMENT_PROCESSOR.ACCOUNT_DETAILS_LINE_MATCH_REGEX)
        self.accountDetailsProcessor.SetFetchFunction(process_card_number)
        self.statementAmountLineProcessor.initialise()

    def create_transaction_table(self):
        transactions = []
        dates = self.dateLineProcessor.GetValues()
        amounts = self.amountLineProcessor.GetValues()
        descriptions = self.descriptionLineProcessor.GetValues()
        [transactions.append({"txnDescription":descriptions[i],"txnAmount":amounts[i], \
                                "txnTimestamp":dates[i]}) for i in range(1,len(dates))]
        return transactions

    def getCalculatedAmounts(self,amounts):
        wrongC = 0
        wrongD = 0
        credit = 0
        debit = 0
        for i in range(1,amounts["length"] + 1):
            amountVal = amounts[i]['value']
            if amountVal["txnType"] == 'DEBIT':
                debit = debit + amountVal['amount']
            if amountVal["txnType"] == 'CREDIT':
                credit = credit + amountVal['amount']
            if "inverse" in amountVal:
                if amountVal["inverse"] and amountVal["txnType"] == 'DEBIT':
                    wrongC = wrongC + amountVal["amount"]
                if amountVal["inverse"] and amountVal["txnType"] == 'DEBIT':
                    wrongD = wrongD + amountVal["amount"]
        return wrongC,wrongD,credit,debit

    def process(self):
        transactions = []
        for line in self.lines.splitlines():
            self.amountLineProcessor.process(line)
            self.descriptionLineProcessor.process(line)
            self.dateLineProcessor.process(line)
            self.statementAmountLineProcessor.process(line)
            self.accountDetailsProcessor.process(line)
        dates = self.dateLineProcessor.GetValues()
        amounts = self.amountLineProcessor.GetValues()
        descriptions = self.descriptionLineProcessor.GetValues()
        statementAmounts = self.statementAmountLineProcessor.GetValues()
        cardDetails = self.accountDetailsProcessor.GetValues()
        
        if cardDetails["length"] != 1:
            print("Unable to get card details")
            return False,{}

        accountNumber = cardDetails[1]['value']['cardNumber']

        #Cross verifying account number details
        accountNumberProvided = self.accountDetails.GetaccountNumber()
        if accountNumber[:2] + accountNumber[-4:] != accountNumberProvided[:2] + accountNumber[-4:]:
            print("Mismatch in Account Number Provided %s and Account Number %s" \
                                            %(accountNumberProvided,accountNumber))
            return False,{}
        if self.statementAmountLineProcessor.GetTotalValues() != 5:
            print("Error in getting proper statement values")
            return False,{}
        
        #Get the statement values
        openingBalance = statementAmounts[1]['value']['amount']
        payments = statementAmounts[2]['value']['amount']
        debits = statementAmounts[3]['value']['amount']
        finance = statementAmounts[4]['value']['amount']
        totalDues = statementAmounts[5]['value']['amount']
        if 'inverse' in statementAmounts[5]['value']:
            if statementAmounts[5]['value']['inverse']:
                totalDues = 0 - totalDues
        if 'inverse' in statementAmounts[1]['value']:
            if statementAmounts[1]['value']['inverse']:
                openingBalance = 0 - openingBalance

        #Observed an error with error credit 
        hdfcBankErrorCredit,hdfcBankErrorDebit,paymentsCal,debitsCal = self.getCalculatedAmounts(amounts)
        errorDiff = openingBalance - payments + debits + finance + hdfcBankErrorDebit - hdfcBankErrorCredit - totalDues
        extra_payments_or_debits = 0
        if abs(payments-paymentsCal) < HDFCCCStatementProcessor.HDFC_PAYMENTS_DEBITS_ERROR_THRESHOLD:
            if abs(payments-paymentsCal) != 0:
                extra_payments_or_debits = extra_payments_or_debits + payments - paymentsCal
        else:
            print("Mismatch in collected summary of statements and summary")
            return False,{}
        
        if abs(debits-debitsCal + finance) < HDFCCCStatementProcessor.HDFC_PAYMENTS_DEBITS_ERROR_THRESHOLD:
            if abs( debits-debitsCal + finance) != 0:
                extra_payments_or_debits = extra_payments_or_debits - ( debits - debitsCal + finance )
        else:
            if abs( debits - debitsCal ) < HDFCCCStatementProcessor.HDFC_PAYMENTS_DEBITS_ERROR_THRESHOLD:
                if abs(debits-debitsCal) != 0:
                    extra_payments_or_debits = extra_payments_or_debits - (debits-debitsCal)
            else:
                print("Mismatch in collected summary of statements and summary")
                return False,{}

        if abs(errorDiff) > HDFCCCStatementProcessor.HDFC_DUE_ERROR_THRESHOLD:
            if abs(abs(errorDiff) - finance) > HDFCCCStatementProcessor.HDFC_DUE_ERROR_THRESHOLD:
                print("Mismatch in collected summary of payments")
                return False,{}

        totalValueCalculated = 0
        for i in range(1,amounts['length'] + 1):
            amount = amounts[i]['value']['amount']
            txnType = amounts[i]['value']['txnType']
            if txnType == 'CREDIT':
                totalValueCalculated = totalValueCalculated - amount
            else:
                totalValueCalculated = totalValueCalculated + amount
        #Dates count and descriptions count should be same
        if len(dates) != len(amounts):
            print("Failed to get all entries")
            return False,transactions
        #Handling an edge case where the description comes in between last date and amout entries
        if descriptions["length"] < amounts["length"]:
            amountLastLine = amounts[amounts["length"]]['line']
            dateLastLine = dates[dates["length"]]['line']
            self.descriptionLineProcessor.OverrideAndProcess(
                            self.lines.splitlines()[dateLastLine:amountLastLine-1])    
         #Dates count and descriptions count should be same
        descriptions = self.descriptionLineProcessor.GetValues()
        if len(descriptions) != len(amounts):
            print("Failed to get all entries")
            return False,transactions

        currentTransactions = self.create_transaction_table()
        lineNumber = -1
        if abs(extra_payments_or_debits) > 0:
            extraTxn = {
                 "txnTimestamp" : currentTransactions[-1]['txnTimestamp'],
                 "txnDescription" :{
                        "value":{
                                "description":"ADJUST_PAYMENTS_DATA"
                                },
                        'line':lineNumber
                    },
                 "txnAmount" : {
                    "value" : {
                            "amount":Decimal(extra_payments_or_debits),
                            "txnType":"CREDIT"
                            },
                    "line" : lineNumber,
                 }
            }
            if extra_payments_or_debits < 0:
                extraTxn['txnAmount']['value']['txnType'] = 'DEBIT'
            currentTransactions.append(extraTxn)
            lineNumber = lineNumber - 1
        return True,currentTransactions
