import flask
import azure.cosmos.exceptions as exceptions
from azure.cosmos import CosmosClient, PartitionKey

ENDPOINT = ""
KEY=""
DATABASE_NAME="Cities"
key_path = PartitionKey(path="/partitionkey")
client = CosmosClient(url=ENDPOINT, credential=KEY)
database = client.create_database_if_not_exists(id=DATABASE_NAME)
print("Database\t", database.id)
container = database.create_container_if_not_exists(
    id="city", partition_key=key_path, offer_throughput=400
)
print("Container\t", container.id)
def replace_item(container, doc_id,partition_key,city):
    print('\n1.6 Replace an Item\n')

    read_item = container.read_item(item=doc_id, partition_key=partition_key)
    read_item['city'] = city
    print(read_item)
    response = container.replace_item(item=read_item, body=read_item)
    print('Replaced Item\'s Id is {0}, new subtotal={1}'.format(response['id'], response['city']))

replace_item(container,"usercity","11111","gaza")