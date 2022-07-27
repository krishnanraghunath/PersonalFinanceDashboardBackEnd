#CSV Fields for Bank Record Processor
class CSVFieldsBankRecordProcessor:
    DATE = 'DATE'
    DESC = 'Narration'
    VALUE_DATE = 'Value Dat'
    DEBIT = 'Debit Amount'
    CREDIT =  'Credit Amount'
    REF_NO = 'Chq/Ref Number'
    CLOSING_BAL = 'Closing Balance'


class APIErrors:
    APINFOUND = 'API Not Found'
    INTERROR = "Internal Error While Processing the Request"
    REQUESTERROR = "Request is not correct"

STATEMENTS_UPLOAD_BUCKET = 'transactionfilesuploads'


class PDF_STATEMENT_PROCESSOR:
    AMOUNT_LINE_START_REGEX = ['^Amount \(Rs.\)']
    DATE_LINE_START_REGEX = ['^Date$']

class KOTAK_CC_STATEMENT_PROCESSOR:
    AMOUNT_LINE_STOP_REGEX = ['Page [d] of [d]','SMS EMI']
    AMOUNT_LINE_MATCH_REGEX = ['^([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+).[0-9][0-9]']
    DESCRIPTION_LINE_START_REGEX = ['^Transaction details from']
    DESCRIPTION_LINE_STOP_REGEX = ['^Total Purchase \& Other Charges$','^Spends Area$','^CRN: [0-9]+$']
    DESCRIPTION_LINE_NO_MATCH_REGEX = [ '^(^Primary Card Transactions-)',
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
                                        ]
    DATE_LINE_STOP_REGEX =  ['^Transaction details from']
    ACCOUNT_DETAILS_LINE_START_REGEX  = ['^Total Credit Limit$']
    ACCOUNT_DETAILS_LINE_STOP_REGEX   = ['^Retail Purchases and Cash Transactions$']
    ACCOUNT_DETAILS_LINE_MATCH_REGEX  = ['^Primary Card Transactions-']



class HDFC_CC_STATEMENT_PROCESSOR:
    AMOUNT_LINE_START_REGEX = ['^Amount \(in Rs.\)']
    AMOUNT_LINE_STOP_REGEX = ['Page [d] of [d]','SMS EMI','^Opening Balance$']
    STATEMENT_AMOUNT_LINE_START_REGEX = ['^Opening$']
    STATEMENT_AMOUNT_LINE_STOP_REGEX = ['^Overlimit$']
    DESCRIPTION_LINE_START_REGEX = ['Transaction Description$']
    DESCRIPTION_LINE_STOP_REGEX = ['^Amount \(in Rs.\)$','(^Domestic Transactions$)']
    DESCRIPTION_LINE_NO_MATCH_REGEX = [ '^HARIKRISHNAN$',
                                        '^(\d{2})/(\d{2})/(\d{4})$', 
                                        '^(\d{2})/(\d{2})/(\d{4}) (\d{2}):(\d{2}):(\d{2})$',
                                        '^([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+).[0-9][0-9]$',
                                        '^([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+).[0-9][0-9] Cr$',
                                        '^Feature Reward$',
                                        '^Points$']
    DATE_LINE_STOP_REGEX = ['^Transaction details from', '^Opening Balance$']
    ACCOUNT_DETAILS_LINE_START_REGEX  = ['^Statement for HDFC Bank Credit Card$']
    ACCOUNT_DETAILS_LINE_STOP_REGEX   = ['^Payment Due Date$']
    ACCOUNT_DETAILS_LINE_MATCH_REGEX  = ['Card No:']
    
class ICICI_CC_STATEMENT_PROCESSOR:
    AMOUNT_LINE_START_REGEX = ['International Spends$','Transaction Details']
    AMOUNT_LINE_STOP_REGEX = ['Earned','^No. of Installments$','Page (\d{1}) of (\d{1})']
    AMOUNT_LINE_NO_MATCH_REGEX = ['^(\d{10})$','^([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+).[0-9][0-9] USD$']
    STATEMENT_AMOUNT_LINE_START_REGEX = ['^Total Amount due$']
    STATEMENT_AMOUNT_LINE_STOP_REGEX = ['^Minimum Amount due$']
    STATEMENT_AMOUNT_LINE_MATCH_REGEX = ['^`([0-9]{1,3},([0-9]{3},)*[0-9]{3}|[0-9]+).[0-9][0-9]']
    SERIAL_LINE_START_REGEX = ['^Amount \(in`\)$','^Transaction Details$']
    SERIAL_LINE_STOP_REGEX = ['Page (\d{1}) of (\d{1})']
    SERIAL_LINE_MATCH_REGEX = ['^(\d{10})$']

