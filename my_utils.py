from collections import OrderedDict
from flask import url_for


def make_api_url(action, id):  # not used - delete
    new_url =  url_for(action, id=id, _external=True)
    return new_url


class DictSerializable(object):
	def _asdict(self):
		result = OrderedDict()
		for key in self.__mapper__.c.keys():
			result[key] = getattr(self, key)
		return result