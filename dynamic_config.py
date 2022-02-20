import json, os.path
class DynamicConfig:
	def __init__(self, file="dynamic_config.json"):
		object.__setattr__(self, "_file", file)

		if os.path.exists(file):
			_data = json.loads(open(file, "r").read())
		else:
			_data = {}
			open(file, "w").write(json.dumps(_data))

		object.__setattr__(self, "_data", _data)

	def save(self):
		open(self._file, "w").write(json.dumps(self._data))

	def __getattr__(self, attr):
		return self._data[attr]

	def __setitem__(self, attr, value):
		self._data[attr] = value

	def __setattr__(self, attr, value):
		self._data[attr] = value
		self.save()

	def __delattr__(self, attr):
		del self._data[attr]


#dynamic_config = DynamicConfig()