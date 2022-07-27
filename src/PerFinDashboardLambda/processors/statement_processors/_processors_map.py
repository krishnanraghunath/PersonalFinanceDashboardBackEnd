from PerFinDashboardLambda.processors.statement_processors.hdfc_cc_statement_processor import HDFCCCStatementProcessor
from PerFinDashboardLambda.processors.statement_processors.icici_cc_statement_processor import ICICICCStatementProcessor
from PerFinDashboardLambda.processors.statement_processors.kotak_cc_statement_processor import KotakCCStatementProcessor

ProcessorsMapping = {
    'HDFC_BANK:CREDITCARD:application/pdf' : HDFCCCStatementProcessor,
    'KOTAK_BANK:CREDITCARD:application/pdf' : KotakCCStatementProcessor,
    'ICICI_BANK:CREDITCARD:application/pdf' : ICICICCStatementProcessor
}