import pytest

from bessie import Endpoint, RequiredParameterMissingError

endpoint = Endpoint('GET', 'posts/all', ['user_id'])
endpoint_with_path_params = Endpoint('GET', 'posts/all/<user_id>')
sep = '/'

def format_endpoint(method, path):
	return '{} {}'.format(method, path) 

def test_match():
	did_match = endpoint.match(format_endpoint(endpoint.method, endpoint.path), sep)
	assert did_match

def test_method_does_not_match():
	did_match = endpoint.match(format_endpoint('', endpoint.path), sep)
	assert not did_match

def test_path_does_not_match():
	did_match = endpoint.match(format_endpoint(endpoint.method, ''), sep)
	assert not did_match

def test_nothing_matches():
	did_match = endpoint.match(format_endpoint('', ''), sep)
	assert not did_match

def test_match_with_path_params():
	path = endpoint_with_path_params.path.replace('<', '').replace('>', '')
	did_match = endpoint_with_path_params.match(format_endpoint(endpoint_with_path_params.method, path), sep)
	assert did_match

def test_validate_with_required_params():
	assert endpoint.validate({'user_id': '12345'}, None) is None

def test_invalid_required_params():
	with pytest.raises(RequiredParameterMissingError):
		endpoint.validate(None, None) 

def test_validate_with_path_params():
	assert endpoint_with_path_params.validate(None, {'user_id', '12345'}) is None

def test_invalid_path_params():
	with pytest.raises(RequiredParameterMissingError):
		endpoint_with_path_params.validate(None, None) 


