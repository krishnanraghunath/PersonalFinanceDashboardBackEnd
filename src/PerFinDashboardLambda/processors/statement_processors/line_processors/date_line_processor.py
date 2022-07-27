from PerFinDashboardLambda.processors.statement_processors.line_processors.regex_line_processor import RegexLineProcessor
import datetime

class DateLineProcessor(RegexLineProcessor):
    def __init__(self):
        RegexLineProcessor.__init__(self)
        self.set_match_regexes(["^(\d{2})/(\d{2})/(\d{4})$",
        "^(\d{2})/(\d{2})/(\d{4}) (\d{2}):(\d{2}):(\d{2})$"])
        self.SetFetchFunction(self.process_date)
        pass

    def process_date(self,line):
        try:
            line = line.split(' ')[0] #Removing the HH:MM:SS at the end if present
            dateStrVals = line.split('/')
            day = int(dateStrVals[0])
            month = int(dateStrVals[1])
            year = int(dateStrVals[2])
            dt = datetime.datetime(year=year, month=month, day=day)
            # Also checking it if is a later date than say 01/01/2015 and less than a near future date
            # (it should be tomorrow ideally) --> TODO: Make sensible comparison
            # (some valid close enough date and  which will be alwasy in past in terms of statements)
            if datetime.datetime(year=2015, month=1, day=1) < dt < datetime.datetime(year=2025, month=1, day=1):
                return {'date':line}
        except:
            pass

