from datetime import date
from PerFinDashboardLambda.processors.statement_processors.line_processors.amount_line_processor import AmountLineProcessor
from PerFinDashboardLambda.processors.statement_processors.line_processors.regex_line_processor import RegexLineProcessor
from PerFinDashboardLambda.processors.statement_processors.pdf_statement_processor import PDFStatementProcessor
from PerFinDashboardLambda.constants import ICICI_CC_STATEMENT_PROCESSOR
from decimal import Decimal

def process_statement_amount(line):
    line = line.replace(',','')
    amountLine = line.split('`')[1].split(' ')[0]
    amount = Decimal(amountLine)
    try:
        if line.split('`')[1].split(' ')[1] in ['CR','cr','Cr']:
            amount = 0 - amount
    except:
        pass
    return {'amount':amount}

def process_serial(line):
    return line

class ICICICCStatementProcessor(PDFStatementProcessor):
    def __init__(self,fileName,accountDetails):
        PDFStatementProcessor.__init__(self,fileName,accountDetails)
        self.statementAmountLineProcessor = AmountLineProcessor()
        self.serialNumberProcessor = RegexLineProcessor()
        self.amountLineProcessor.set_start_regexes(ICICI_CC_STATEMENT_PROCESSOR.AMOUNT_LINE_START_REGEX)
        self.amountLineProcessor.set_stop_regexes(ICICI_CC_STATEMENT_PROCESSOR.AMOUNT_LINE_STOP_REGEX)
        self.amountLineProcessor.set_no_match_regexes(ICICI_CC_STATEMENT_PROCESSOR.AMOUNT_LINE_NO_MATCH_REGEX)
        self.statementAmountLineProcessor.set_start_regexes(ICICI_CC_STATEMENT_PROCESSOR.STATEMENT_AMOUNT_LINE_START_REGEX)
        self.statementAmountLineProcessor.set_stop_regexes(ICICI_CC_STATEMENT_PROCESSOR.STATEMENT_AMOUNT_LINE_STOP_REGEX)
        self.statementAmountLineProcessor.set_match_regexes(ICICI_CC_STATEMENT_PROCESSOR.STATEMENT_AMOUNT_LINE_MATCH_REGEX)
        self.statementAmountLineProcessor.SetFetchFunction(process_statement_amount)
        self.serialNumberProcessor.set_start_regexes(ICICI_CC_STATEMENT_PROCESSOR.SERIAL_LINE_START_REGEX)
        self.serialNumberProcessor.set_stop_regexes(ICICI_CC_STATEMENT_PROCESSOR.SERIAL_LINE_STOP_REGEX)
        self.serialNumberProcessor.set_match_regexes(ICICI_CC_STATEMENT_PROCESSOR.SERIAL_LINE_MATCH_REGEX)
        self.serialNumberProcessor.SetFetchFunction(process_serial)
        self.serialNumberProcessor.initialise()
        self.statementAmountLineProcessor.initialise()
        

    def create_transaction_table(self,dates,amounts,descriptions):
        transactions = []
        length = amounts['length']
        for i in range(1,length+1):
            if i  in amounts['deleted']:
                continue
            transactions.append({"txnDescription":descriptions[i],"txnAmount":amounts[i], \
                                "txnTimestamp":dates[i]})
        return transactions

    def get_payments_debits(self,amounts):
        payments = 0
        debits = 0

        for i in range(1,amounts['length'] + 1):
            if i in amounts['deleted']:
                continue
            if amounts[i]['value']['txnType'] == 'DEBIT':
                debits = debits + amounts[i]['value']['amount']
            else:
                payments = payments + amounts[i]['value']['amount']
        return payments,debits
            


    def process(self):
        accountNumber = ''
        for line in self.lines.splitlines():
            self.amountLineProcessor.process(line)
            self.statementAmountLineProcessor.process(line)
            self.serialNumberProcessor.process(line)
            if 'XXXXXXXX' in line:
                accountNumber = line
        
        amounts = self.amountLineProcessor.GetValues()
        statementAmounts = self.statementAmountLineProcessor.GetValues()
        serials = self.serialNumberProcessor.GetValues()
        
        if statementAmounts['length'] != 5:
            return False,{}
        
        totalDue = statementAmounts[1]['value']['amount']
        prevBalance = statementAmounts[2]['value']['amount']
        debits = statementAmounts[3]['value']['amount']
        cash = statementAmounts[4]['value']['amount']
        payments = statementAmounts[5]['value']['amount']
        if totalDue != (prevBalance + debits + cash - payments):
            return False,{}
        descriptions = {"length":0}
        dates = {"length":0}
        lineVals = self.lines.splitlines()
        duplicateIndices = []
        refs = []
        for i in range(1,serials["length"] + 1):
            if serials[i]['value'] not in refs:
                refs.append(serials[i]['value'])
            else:
                duplicateIndices.append(i)
            line = serials[i]['line']
            descriptionLine = line + 1
            dateLine = line - 3
            descriptionVal = lineVals[descriptionLine]
            dateVal = lineVals[dateLine]
            if 'XXXXXXXX' in descriptionVal:
                accountNumber = descriptionVal 
                descriptionVal =  lineVals[int(line)+3]
                descriptionLine = descriptionLine + 3
            descriptions[i] = {"line":descriptionLine,"value":{ "description":descriptionVal}}
            dates[i] = {"line":dateLine,"value":{ "date":dateVal}}
        descriptions['length'] = len(descriptions)-1
        dates['length'] = len(dates)-1
        amounts['deleted'] = duplicateIndices
        dates['deleted'] = duplicateIndices
        descriptions['deleted'] = duplicateIndices

        #Cross verifying account number details
        accountNumberProvided = self.accountDetails.GetaccountNumber()
        if accountNumber[:2] + accountNumber[-4:] != accountNumberProvided[:2] + accountNumber[-4:]:
            print("Mismatch in Account Number Provided %s and Account Number %s" \
                                            %(accountNumberProvided,accountNumber))
            return False,{}

        if descriptions['length'] != amounts['length']:
            self.print(dates,amounts,descriptions)
            return False,{}
        
        if(amounts["length"] != dates["length"]):
            self.print(dates,amounts,descriptions)
            return False,{}

        paymentsCal,debitsCal = self.get_payments_debits(amounts)
        if payments - paymentsCal != 0:
            return False,{}
        if debits - debitsCal != 0:
            return False,{}

        currentTransactions = self.create_transaction_table(dates,amounts,descriptions)
        return True,currentTransactions
