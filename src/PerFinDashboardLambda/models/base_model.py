from json import loads
from traceback import print_exc as trace
class BaseModel:

    '''For each field 2 functions will be created
     fn:<fieldName> () --> Set Value
    fn: Get<fieldName > () --> Get Value
    '''
    def __init__(self,object=None,fieldsMap={}):
        for field in self.fields:
            setattr(self,field,self._function_set('_' + field))
            setattr(self,'Get'+field,self._function_get('_' + field))
        if object!=None:
            self.ingest(object,fieldsMap)

    '''
    object ==> JSON Object / Json string
    fieldsMap ==> json param -> fields (defined)
    '''
    def ingest(self,object,fieldsMap={}):
        if object == None:
            return self
        try:
            jsonObject = object
            if isinstance(object,str):
                jsonObject = loads(object)
            '''Copy the fields to class based on field -> json Field map'''
            [self._set_value('_'+x,jsonObject[fieldsMap[x]]) for x in
                        filter(lambda y:fieldsMap[y] in jsonObject,
                               filter(lambda z:z in fieldsMap,self.fields))]
            '''Copy the all the deined fields (assuming field == jsonField name for all fields)'''
            [self._set_value('_' + x, jsonObject[x]) for x in
                        filter(lambda y: y in jsonObject,self.fields)]
        except:
            pass
        return self

    '''Return a dict of field -> value'''
    def __invert__(self):
        kwargs = {}
        for field in self.fields:
            try:
                if getattr(self,'_'+field) != None:
                    kwargs[field] = getattr(self,'_'+field)
            except:
                pass
        return kwargs

    def _function_set(self,field):
        return lambda x:self._set_value(field,x)

    def _function_get(self, field):
        return lambda : self._get_value(field)

    def _set_value(self,field,value):
        setattr(self,field,value)
        return self

    def _get_value(self,field):
        try:
            return getattr(self,field)
        except:
            return None


