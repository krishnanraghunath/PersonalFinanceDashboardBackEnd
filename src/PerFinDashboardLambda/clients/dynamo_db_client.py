import boto3
import traceback

class DynamoDBClient:
    def __init__(self):
        self.client = None
        self.table = None
        self.MAX_LIMIT = 10

    def initialise(self):
        try:
            self.client = boto3.resource('dynamodb')
        except Exception as e:
            print("Unable to create Dynamo DB Resource : %s"%(str(e)))

    def set_table(self,table_name):
        if self.client:
            self.table = self.client.Table(table_name)
        else:
            print("Client is not initialised to set the Table")

    '''Query DDB Items'''
    def query(self,queryInput):
        try:
            _response = []
            _response = self.table.query(**~queryInput)
            lastEvalKey = None
            if 'lastEvaluatedKey' in _response:
                lastEvalKey = _response['lastEvaluatedKey']
            items = []
            if 'Items' in _response:
                items = _response['Items']
            return True,items,lastEvalKey
        except:
            traceback.print_exc()
            print(~(queryInput))
            return False,[],None

    '''Get DDB Items'''
    def get(self,getInput):
        try:
            _response = self.table.get_item(**~getInput)
            if 'lastEvaluatedKey' in _response:
                lastEvalKey = _response['lastEvaluatedKey']
            if 'Item' in _response:
                return True,_response['Item']
        except:
            traceback.print_exc()
            print(~(getInput))
        return False,None

    '''Update DDB Items'''
    def update(self,updateInput):
        try:
            _response = self.table.update_item(**~updateInput)
            #TODO : _response needs to be analysed for failure
            return True,_response
        except:
            traceback.print_exc()
            print(~(updateInput))
        return False,None

    '''Write DDB Item'''
    def write_item(self, writeInput):
        try:
            _response = self.table.put_item(**~writeInput)
            # TODO : _response needs to be analysed for failure
            return True, _response
        except:
            traceback.print_exc()
            print(~(writeInput))
        return False, {}

    
        '''Write DDB Item'''
    def delete_item(self, deleteInput):
        try:
            _response = self.table.delete_item(**~deleteInput)
            # TODO : _response needs to be analysed for failure
            return True, _response
        except:
            traceback.print_exc()
            print(~(deleteInput))
        return False, {}

    '''Write DDB Items in batch'''
    def batch_write_items(self,batchWriteInput):
        try:
            _response = self.client.batch_write_item(**~batchWriteInput)
            #TODO : _response needs to be analysed for failure
            return True,_response
        except:
            traceback.print_exc()
            print(~(batchWriteInput))
        return False, {}




