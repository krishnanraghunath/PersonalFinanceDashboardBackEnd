from PerFinDashboardLambda.clients.dynamo_db_client import DynamoDBClient
from PerFinDashboardLambda.models.ddb.ddb_batch_write_items_request_model import DDBBatchWriteItemsRequestModel
from PerFinDashboardLambda.models.ddb.ddb_write_item_request_model import DDBWriteItemRequestModel

class BaseTableClient:
    DEFAULT_QUERY_LIMIT = 10
    DEFAULT_FETCH_LIMIT = 10
    DEFAULT_WRITE_SIZE = 25
    def __init__(self,dbType):
        self.db_client = DynamoDBClient()
        self.db_client.initialise()
        self.tableName = dbType.TABLE_NAME
        self.db_client.set_table(self.tableName)
        self.dbType = dbType
        self._write_items_list = []

    def batch_write_items(self,force = False):
        if len(self._write_items_list) == 0:
            return True
        if len(self._write_items_list) == self.DEFAULT_WRITE_SIZE or force:
            status,response = self.db_client.batch_write_items(
                DDBBatchWriteItemsRequestModel()
                    .RequestItems({self.tableName:self._write_items_list}))
            if 'UnprocessedItems' in response:
                if len(response['UnprocessedItems']) > 0:
                    print("%s: There are unprocessed Items!!"%self.tableName)
                    print(response['UnprocessedItems'])
            self._write_items_list = []
            return status
        else:
            return False

    def get_item(self,getItemRequest):
        response,result = self.db_client.get(getItemRequest)
        if response:
            return True,self.dbType(result)
        return False,None

    def query_items(self,queryItemRequest):
        if queryItemRequest.GetLimit() == None:
            queryItemRequest.Limit(BaseTableClient.DEFAULT_QUERY_LIMIT)
        items_count = queryItemRequest.GetLimit()
        items = []
        lastKey = 1
        while lastKey!=None and items_count > 0:
            response,_items,lastKey = self.db_client.query(queryItemRequest)
            queryItemRequest.ExclusiveStartKey(lastKey)
            items.extend(_items[:items_count])
            items_count = queryItemRequest.GetLimit() - len(items)
        if items_count == 0:
            lastKey = self.dbType(items[-1])
        else:
            lastKey = self.dbType()
        return [self.dbType(item) for item in items],lastKey

    def write_item(self,item):
        response,result = self.db_client.write_item(
            DDBWriteItemRequestModel()
                .Item(~item)
        )
        return response

    def update_item(self,updateItemRequest):
        response,result = self.db_client.update(updateItemRequest)
        return response

    def query_all(self,queryItemRequest):
        queryItemRequest.Limit(100)
        lastKey = 1
        items = []
        while lastKey!=None:
            response,_items,lastKey = self.db_client.query(queryItemRequest)
            queryItemRequest.ExclusiveStartKey(lastKey)
            items.extend(_items)
        return [self.dbType(item) for item in items]

    def add_item(self,itemRequest):
        put_request = {'PutRequest':{'Item':~itemRequest}}
        self._write_items_list.append(put_request)
        self.batch_write_items()
