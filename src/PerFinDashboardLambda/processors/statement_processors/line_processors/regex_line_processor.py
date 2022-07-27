
import re
'''
Line Processor based on Regex on only for following single purpose
1 -> For a series of inputs
2 -> Decide when processor should get activated based on start regexes 
3 -> See if the values are according to the format if it is activated based on match regex
4 -> Decide when processor should get deactivated based on stop egex
'''
class RegexLineProcessor:
    def __init__(self):
        self.__processing_start_regexes = []
        self.__processing_stop_regexes = []
        self.__processing_match_regexes = []
        self.__processing_no_match_regexes = []
        self._processing = False
        self._processing_start_regexes = []
        self._processing_stop_regexes = []
        self._processing_match_regexes = []
        self._processing_no_match_regexes = []
        self._fetch_value_function = None
        self._pre_process_line = None
        self._counter = 0
        self._value_counter = 0
        self._values = {"length":0}
        self.initialised = False
        pass

    def initialise(self):
        self.initialised = True
        #All the regexes will be used with OR combination, i.e if any of hte regex in a list matches that would be fine
        self._processing_start_regexes = list(map(lambda y:re.compile(y),self.__processing_start_regexes))
        self._processing_stop_regexes = list(map(lambda y: re.compile(y), self.__processing_stop_regexes))
        self._processing_match_regexes = list(map(lambda y: re.compile(y), self.__processing_match_regexes))
        self._processing_no_match_regexes = list(map(lambda y: re.compile(y), self.__processing_no_match_regexes))

    def process(self,line):
        if self.initialised ==False:
            raise Exception('Regex Processor is not initialised.')
        self._counter = self._counter + 1
        line = line.strip()
        for stop_regex in self._processing_stop_regexes:
            if stop_regex.search(line):
                self._processing =  False
                return False
        if self._processing:
            if len(list(filter(lambda y:y.search(line)!=None,self._processing_no_match_regexes))) > 0:
                return False
            for match_regex in self._processing_match_regexes:
                if match_regex.search(line):
                    if self._pre_process_line:
                        line = self._pre_process_line(line)
                    _value = self._fetch_value_function(line)
                    if _value:
                        self._value_counter = self._value_counter + 1
                        self._values[self._value_counter] = {}
                        self._values[self._value_counter]['value'] = _value
                        self._values[self._value_counter]['line'] = self._counter
                        self._values['length'] = self._value_counter
                        return True
                    return False

        for start_regex in self._processing_start_regexes:
            if start_regex.search(line):
                self._processing = True
                return False

    def GetTotalLinesProcessed(self):
        return self._counter

    def GetTotalValues(self):
        return self._value_counter

    def SetFetchFunction(self,function):
        self._fetch_value_function = function

    def SetPreProcessFunction(self,function):
        self._pre_process_line = function


    def set_start_regexes(self,start_regex = []):
        self.__processing_start_regexes = start_regex
        self.initialise()

    def set_stop_regexes(self,stop_regex = []):
        self.__processing_stop_regexes = stop_regex
        self.initialise()

    def set_match_regexes(self,match_regex = []):
        self.__processing_match_regexes = match_regex
        self.initialise()

    def set_no_match_regexes(self,match_regex = []):
        self.__processing_no_match_regexes = match_regex
        self.initialise()

    def GetValues(self):
        return self._values

    #Overriding the start checks only.
    def OverrideAndProcess(self,lines):
        self._processing = True 
        for line in lines:
            self.process(line)
        self._processing = False
