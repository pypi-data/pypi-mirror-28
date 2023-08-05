import re

class RequiredParameterMissingError(Exception):
	pass


class Endpoint(object):

	path_param_matching_regex = r'<(\w+)>'

	def __init__(self, method, path, required_params=None):
		self.method = method
		self.path = path

		self.required_params = required_params
		self.path_params = re.findall(self.path_param_matching_regex, path)

	def __repr__(self):
		return '{}({}, {})'.format(self.__class__.__name__, self.method, self.path)

	def match_part(self, part, part_to_match):
		return part == part_to_match

	def match(self, m, separator):
		possible_paths = []

		msplit = m.split(' ')
		method_to_match, path_to_match = msplit[0], msplit[1]

		if self.method != method_to_match:
			return False

		parts = self.path.replace('<', '').replace('>', '').split(separator)
		parts_to_match = path_to_match.split(separator)

		if len(parts) != len(parts_to_match):
			return False

		for idx, part in enumerate(parts):
			part_to_match = parts_to_match[idx]
			if not self.match_part(part, part_to_match):
				return False

		return True

	def validate(self, params=None, path_params=None):

		if not params: 
			params = []

		if not path_params:
			path_params = []

		missing_params = [param for param in self.required_params if param not in params] if self.required_params else []
		missing_params += ['{} (path param)'.format(param) for param in self.path_params if param not in path_params] if self.path_params else []

		if missing_params:
			raise RequiredParameterMissingError('The following required parameters are missing: {}'.format(', '.join(missing_params)))