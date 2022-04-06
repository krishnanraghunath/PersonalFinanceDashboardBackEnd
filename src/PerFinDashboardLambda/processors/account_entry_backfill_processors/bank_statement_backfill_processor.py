from PerFinDashboardLambda.models.dao.accounting_entry_table_model import AccountingEntryTableModel
from PerFinDashboardLambda.dao.accounting_entry_table_client import AccountingEntryTableClient
from uuid import uuid4 as UUID
from time import time
from datetime import datetime
from decimal import Decimal
class BankStatementBackfillProcessor:
    CSV_Fields = ['Date', 'Narration', 'Value Dat', 'Debit Amount', \
                   'Credit Amount', 'Chq/Ref Number', 'Closing Balance']
    CSV_Delimiter = ','
    CSV_Delimiter_Replacer = '$%^&'
    DATE_TIME_FORMAT =  "%d/%m/%y"

    def __init__(self):
        self.accoutEntryTableClient = AccountingEntryTableClient()
        pass

    def execute(self,data,accountId):
        data = data.splitlines()
        if len(data) < 2:
            print("CSV Should have atleast 1 entry")
            return
        headers = list(map(lambda x:x.strip(),data[0].split(BankStatementBackfillProcessor.CSV_Delimiter)))
        comp = []
        comp.extend(headers)
        comp.extend(BankStatementBackfillProcessor.CSV_Fields)
        if len(list(filter(lambda x:x not in headers or \
                                    x not in BankStatementBackfillProcessor.CSV_Fields,\
                           comp))) > 0:
            print("Extra fields present for few fields are missing")
            print("Expected Fields => %s"%",".join(BankStatementBackfillProcessor.CSV_Fields))
            print("Present Fields => %s" % ",".join(headers))
            return

        header_index = {}
        for header in headers:
            header_index[header] = headers.index(header)

        for row in data[1:]:
            colCount = row.count(BankStatementBackfillProcessor.CSV_Delimiter)+1
            if colCount < len(headers):
                print("BankStatementBackfillProcessor => Ignore Entry:%s" % row)
                continue
            if colCount > len(headers):
                print("BankStatementBackfillProcessor  Column count is more for row (possible narrative have extra delimeters)")
                # This means the extra commas is part of an field and tht field can only be "Narration"
                narration_start_index = header_index['Narration']
                narration_end_index = narration_start_index + (colCount - len(headers))
                rows_final = row.split(BankStatementBackfillProcessor.CSV_Delimiter)
                rows_original = ','.join(rows_final[:narration_start_index])+',' \
                                        + BankStatementBackfillProcessor.CSV_Delimiter_Replacer.join(
                                            rows_final[narration_start_index:narration_end_index+1])+',' \
                                        + ','.join(rows_final[narration_end_index+1:])

                print("From Row %s to Row %s"%(row,rows_original))
                row = rows_original

            row_data = row.split(',')

            txnDate = row_data[header_index['Date']].strip()
            txnTimestamp = int(datetime.strptime(txnDate,BankStatementBackfillProcessor.DATE_TIME_FORMAT) \
                                .timestamp())
            amtCdt = Decimal(0)
            amtDbt = Decimal(0)
            txnType = 'CREDIT'
            '''Try except if we providie it as empty char instead of 0.00'''
            try:
                amtCdt = Decimal(row_data[header_index['Credit Amount']])
            except:
                pass
            try:
                amtDbt = Decimal(row_data[header_index['Debit Amount']])
            except:
                pass
            amount = amtCdt
            if amtDbt > amtCdt:
                amount = amtDbt
                txnType = 'DEBIT'
            accountEntry = AccountingEntryTableModel() \
                                .internalTxnId(str(UUID())) \
                                .accountId(accountId) \
                                .lastModifiedTimestamp(int(time())) \
                                .externalTxnId(row_data[header_index['Chq/Ref Number']].strip()) \
                                .externalAccountId('UNKNOWN') \
                                .txnDescription(str(row_data[header_index['Narration']].strip().replace
                                               (BankStatementBackfillProcessor.CSV_Delimiter_Replacer,
                                                BankStatementBackfillProcessor.CSV_Delimiter)))\
                                .txnTimestamp(txnTimestamp) \
                                .txnType(txnType) \
                                .amount(amount)
            ##Checking previous transaction with same Reference Number exist for the account if not add it

            if self.accoutEntryTableClient.is_uniq_transaction(accountEntry.GetexternalTxnId(),accountEntry.GettxnTimestamp()):
                self.accoutEntryTableClient.put_accounting_entry(accountEntry)
            else:
                print("BankStatementBackfillProcessor: Skipping already present --> %s"%row)
        self.accoutEntryTableClient.batch_write_items(True)
        print("Execution Completed for %d entries"%(len(data)-1))