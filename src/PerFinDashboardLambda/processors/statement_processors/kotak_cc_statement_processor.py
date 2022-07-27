from PerFinDashboardLambda.processors.statement_processors.pdf_statement_processor import PDFStatementProcessor
from PerFinDashboardLambda.constants import KOTAK_CC_STATEMENT_PROCESSOR

def process_card_number(line):
    try:
        return {'cardNumber':line.split(' ')[-1]}
    except:
        return None

class KotakCCStatementProcessor(PDFStatementProcessor):
    IGNORE_PAYMENTS_ENTRY = [
        'PAYMENT RECEIVED-MOBILE FUNDS TRANSFER',
        'PAYMENT RECEIVED-NEFT',
        'PAYMENT RECEIVED-KOTAK IMPS'
    ]

    def __init__(self,fileName,accountDetails):
        PDFStatementProcessor.__init__(self,fileName,accountDetails)
        # self.amountLineProcessor.set_stop_regexes(KOTAK_CC_STATEMENT_PROCESSOR.AMOUNT_LINE_STOP_REGEX)
        # self.amountLineProcessor.set_match_regexes(KOTAK_CC_STATEMENT_PROCESSOR.AMOUNT_LINE_MATCH_REGEX)
        # self.descriptionLineProcessor.set_start_regexes(KOTAK_CC_STATEMENT_PROCESSOR.DESCRIPTION_LINE_START_REGEX)
        # self.descriptionLineProcessor.set_stop_regexes(KOTAK_CC_STATEMENT_PROCESSOR.DESCRIPTION_LINE_STOP_REGEX)
        # self.descriptionLineProcessor.set_no_match_regexes(KOTAK_CC_STATEMENT_PROCESSOR.DESCRIPTION_LINE_NO_MATCH_REGEX)
        # self.dateLineProcessor.set_stop_regexes(KOTAK_CC_STATEMENT_PROCESSOR.DATE_LINE_STOP_REGEX)
        # self.accountDetailsProcessor.set_start_regexes(KOTAK_CC_STATEMENT_PROCESSOR.ACCOUNT_DETAILS_LINE_START_REGEX)
        # self.accountDetailsProcessor.set_stop_regexes(KOTAK_CC_STATEMENT_PROCESSOR.ACCOUNT_DETAILS_LINE_STOP_REGEX)
        # self.accountDetailsProcessor.set_match_regexes(KOTAK_CC_STATEMENT_PROCESSOR.ACCOUNT_DETAILS_LINE_MATCH_REGEX)
        # self.accountDetailsProcessor.SetFetchFunction(process_card_number)
        self.amountLineProcessor.set_start_regexes([ '^Amount \(Rs.\)'])
        self.amountLineProcessor.set_stop_regexes(['Page [d] of [d]','SMS EMI'])
        self.amountLineProcessor.set_match_regexes(['^([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+).[0-9][0-9]'])


        self.descriptionLineProcessor.set_start_regexes(['^Transaction details from'])
        self.descriptionLineProcessor.set_stop_regexes([
                            '^Total Purchase \& Other Charges$',
                            '^Spends Area$',
                            '^CRN: [0-9]+$'])
        self.descriptionLineProcessor.set_no_match_regexes([
                        '^(^Primary Card Transactions-)',
                        '^(^Retail Purchases and Cash Transactions)',
                        '^(^IN)$',
                        '^(^BANGALORE)$',
                        '^(^Bengaluru)$',
                        '^(^MUMBAI)$',
                        '^(^MYSORE)$',
                        '^(^BANGALORE IN)$',
                        '^(^BENGALURU IN)$',
                        '^(^MALAPPURAM IN)$',
                        '^(^DEVASANDRA IN)$',
                        '^(^PALAKKAD)$',
                        '^(^THRISSUR)$',
                        '^KANNUR$',
                        '^COCHIN$',
                        '^WWW[.]MOBIKWIK[.] IN',
                        '^[0-9]{2}-[\w]+-[2][0-9]{3}$',
                        '^\([0-9]+[.][0-9]{2}[ ][A-Z]{3}\)$',
                        '^(^Other Fees and Charges)$',
                        '^(^EMI and Loans)$',
                        '^(^Payments and Other Credits)$',
                        # 'Convert to EMI\)$',
                        '^IN \(.Convert to EMI\)$',
                        '^BANGALORE IN \(.Convert to EMI\)$',
                        '^My Rewards$',
                        '^Opening Balance$',
                        '^Earned this month$',
                        '^Redeemed this month$',
                        '^Expired this month$',
                        '^Expiring next month$',
                        '^Closing Balance$',
                        '^[+-]?([0-9]+\.?[0-9]*|\.[0-9]+)$'
                        ])
        self.dateLineProcessor.set_start_regexes(['^Date$'])
        self.dateLineProcessor.set_stop_regexes(['^Transaction details from'])


        self.accountDetailsProcessor.set_start_regexes(['^Total Credit Limit$'])
        self.accountDetailsProcessor.set_stop_regexes(['^Retail Purchases and Cash Transactions$'])
        self.accountDetailsProcessor.set_match_regexes(['^Primary Card Transactions-'])
        self.accountDetailsProcessor.SetFetchFunction(process_card_number)

        self.amountLineProcessor.initialise()
        self.descriptionLineProcessor.initialise()
        self.dateLineProcessor.initialise()

    def process(self):
        transactions = []
        for line in self.lines.splitlines():
            self.amountLineProcessor.process(line)
            self.descriptionLineProcessor.process(line)
            self.dateLineProcessor.process(line)
            self.accountDetailsProcessor.process(line)
        #Cross verifying account number details
        cardDetails = self.accountDetailsProcessor.GetValues()
        if cardDetails["length"] != 1:
            print("Unable to get card details")
            return False,{}

        accountNumber = cardDetails[1]['value']['cardNumber']
        accountNumberProvided = self.accountDetails.GetaccountNumber()
        if accountNumber[:2] + accountNumber[-4:] != accountNumberProvided[:2] + accountNumber[-4:]:
            print("Mismatch in Account Number Provided %s and Account Number %s" \
                                            %(accountNumberProvided,accountNumber))
            return False,{}

        dates = self.dateLineProcessor.GetValues()
        amounts = self.amountLineProcessor.GetValues()
        descriptions = self.descriptionLineProcessor.GetValues()
        #Dates count and descriptions count should be same
        if len(dates) != len(descriptions):
            return False,transactions
        #Amount should have an extra value for subtotal
        if len(dates) != (len(amounts) - 1):
            return False,transactions

        totalValueAsPerStatement = amounts[len(amounts)-1]['value']['amount']
        totalValueCalculated = 0
        for i in range(1,len(dates)):
            description = descriptions[i]['value']['description']
            if description in KotakCCStatementProcessor.IGNORE_PAYMENTS_ENTRY:
                continue 
            date = dates[i]['value']['date']
            amount = amounts[i]['value']['amount']
            txnType = amounts[i]['value']['txnType']
            if txnType == 'CREDIT':
                totalValueCalculated = totalValueCalculated - amount
            else:
                totalValueCalculated = totalValueCalculated + amount
            transactions.append(
                {
                    "txnDescription" :descriptions[i],
                    "txnAmount" : amounts[i],
                    "txnTimestamp" : dates[i],
                }
            )

        if(totalValueAsPerStatement != totalValueCalculated):
            print("MisMatch in total values.(Calculated and Provided")
            return False,transactions
        return True,transactions
