from PerFinDashboardLambda.processors.statement_processors.line_processors.regex_line_processor import RegexLineProcessor

class DescriptionLineProcessor(RegexLineProcessor):
    def __init__(self):
        RegexLineProcessor.__init__(self)
        self.set_match_regexes([''])
        self.SetFetchFunction(self.process_description)
        pass

    def process_description(self,line):
        try:
            if line != None and len(line) > 2: #Putting a small restriction on linep
                return {"description":line}
        except:
            return None

