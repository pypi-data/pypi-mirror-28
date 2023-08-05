import pytest

from bessie import *


endpoint = Endpoint('GET', 'posts/all')
endpoint_with_path_param = Endpoint('GET', 'posts/all/<user_id>')

BaseClient.endpoints = [endpoint, endpoint_with_path_param]
client = BaseClient()

def test_has_http_action_attributes():
	actions = [a.lower() for a in ['POST', 'GET', 'PUT', 'PATCH', 'DELETE', 'OPTIONS', 'HEAD']]

	for action in actions:
		assert hasattr(client, action)

def test_endpoint_is_new_instance():
	assert isinstance(client.posts, BaseClient)

def test_find_valid_endpoint():
	assert client.posts.all._find_endpoint(endpoint.method) == endpoint

def test_find_endpoint_with_wrong_method():
	with pytest.raises(InvalidEndpointException):
		client.posts.all._find_endpoint('POST')

def test_find_invalid_endpoint():
	with pytest.raises(InvalidEndpointException):
		client.not_an_endpoint._find_endpoint('GET')

def test_find_valid_path_param_endpoint():
	assert client.posts.all.user_id(12345)._find_endpoint(endpoint_with_path_param.method) == endpoint_with_path_param

def test_path_params_store_key_value():
	key = 'user_id'
	value = 12345
	path_param_call = client.posts.all.user_id(value)

	assert hasattr(path_param_call, 'path_params')
	assert key in path_param_call.path_params
	assert path_param_call.path_params[key] == str(value)

def test_final_request_replaces_path_params():
	key = 'user_id'
	value = 12345
	path_param_call = client.posts.all.user_id(value)
	path_param_call._finalize_request(endpoint_with_path_param.method, {})

	assert path_param_call.request.url == 'posts/all/{}'.format(value)
