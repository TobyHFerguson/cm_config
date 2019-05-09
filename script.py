import cm_client
from cm_client.rest import ApiException
from pprint import pprint
cm_client.configuration.username = 'cloudera'
cm_client.configuration.password = 'Cloudera_123'
api_host = 'http://cl64387-mn0.ukwest.cloudapp.azure.com'
port = '7180'
api_version = 'v19'
api_client = cm_client.ApiClient(api_url)
api_url = api_host + ':' + port + '/api/' + api_version
api_response = cluster_api_instance.read_clusters(view='SUMMARY')
for cluster in api_response.items:
    print cluster.name, -, cluster.full_version
