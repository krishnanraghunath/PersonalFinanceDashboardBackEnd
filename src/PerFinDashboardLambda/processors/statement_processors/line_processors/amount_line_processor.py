from PerFinDashboardLambda.processors.statement_processors.line_processors.regex_line_processor import RegexLineProcessor
from decimal import Decimal

class AmountLineProcessor(RegexLineProcessor):
    def __init__(self):
        RegexLineProcessor.__init__(self)
        self.set_match_regexes(['([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+).[0-9][0-9]'])
        self.SetFetchFunction(self.process_amount)
        pass

    def process_amount(self,line):
        try:
            lineVals = line.upper().replace(',','').split(' ')
            retAmount = {}
            amount = Decimal(lineVals[0])
            txnType = 'DEBIT'
            if len(lineVals) > 1 and lineVals[1] == 'CR':
                txnType = 'CREDIT'
            if amount < 0:
                retAmount["inverse"] = True
                amount = 0 - amount
                if txnType == 'CREDIT':
                    txnType = 'DEBIT'
                else:
                    txnType = 'CREDIT'
            retAmount['amount'] = amount 
            retAmount['txnType'] =  txnType
            return retAmount
        except:
            return None

