from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
import io
from PerFinDashboardLambda.processors.statement_processors.line_processors.amount_line_processor import AmountLineProcessor
from PerFinDashboardLambda.processors.statement_processors.line_processors.date_line_processor import DateLineProcessor
from PerFinDashboardLambda.processors.statement_processors.line_processors.description_line_processor import DescriptionLineProcessor
from PerFinDashboardLambda.processors.statement_processors.line_processors.regex_line_processor import RegexLineProcessor
from PerFinDashboardLambda.constants import PDF_STATEMENT_PROCESSOR

class PDFStatementProcessor:

    def __init__(self,localFileName,accountDetails):
        self.fileName = localFileName
        self.accountDetails = accountDetails
        self.amountLineProcessor = AmountLineProcessor()
        self.descriptionLineProcessor = DescriptionLineProcessor()
        self.dateLineProcessor = DateLineProcessor()
        self.accountDetailsProcessor = RegexLineProcessor()
        #Few Generic initialisations
        self.amountLineProcessor.set_start_regexes(PDF_STATEMENT_PROCESSOR.AMOUNT_LINE_START_REGEX)
        self.dateLineProcessor.set_start_regexes(PDF_STATEMENT_PROCESSOR.DATE_LINE_START_REGEX)
        

    def initialise(self):
        self.amountLineProcessor.initialise()
        self.descriptionLineProcessor.initialise()
        self.dateLineProcessor.initialise()
        self.accountDetailsProcessor.initialise()
        response,self.lines = self._fetch_data()
        return response

    def process(self):
        print("Process method not overridden.")
        return False,None

    def _fetch_data(self):
        fileObject = open(self.fileName,'rb')
        try:
            resMgr = PDFResourceManager()
            retData = io.StringIO()
            TxtConverter = TextConverter(resMgr, retData, laparams=LAParams())
            interpreter = PDFPageInterpreter(resMgr, TxtConverter)
            for page in PDFPage.get_pages(fileObject):
                interpreter.process_page(page)
            return True,retData.getvalue()
        except:
            return False,None        

