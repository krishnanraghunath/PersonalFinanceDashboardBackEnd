class FieldVerify:
    def isNonEmptyString(object):
        if type(object) != type('string'):
            return False 
        if len(object) == 0:
            return False
        return True
    
    def isNonEmptyList(object):
        if type(object) != type([]):
            return False 
        if len(object) == 0:
            return False
        return True
    
    def isTimestampInSeconds(object):
        try:
            timestamp = int(object)
            if timestamp >640636200 and timestamp < 3323010600:
                return True
            return False
        except:
            return False

    def isTimestampInMillis(object):
        try:
            timestamp = int(object)
            if timestamp >640636200000 and timestamp < 3323010600000:
                return True
            return False
        except:
            return False
    
    def isAmount(value):
        try:
            value = float(value)
            if(value >= 0.0):
                return True
            return False
        except:
            return False