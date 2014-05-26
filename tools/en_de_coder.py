import json


class MyEncoder(json.JSONEncoder):

	def default(self,obj):
		d = {}
		d['__class__'] = obj.__class__.__name__
		d['__module__'] = obj.__module__
		d.update(obj.__dict__)
		return d


class MyDecoder(json.JSONDecoder):

	def __init__(self):
		json.JSONDecoder.__init__(self,object_hook=self.dict2object)
	def dict2object(self,d):
		if '__class__' in d:
			class_name = d.pop('__class__')
			module_name = d.pop('__module__')
			module = __import__(module_name)
			class_ = getattr(module,class_name)
			args = dict((key.encode('ascii'),value) for key,value in d.items())
			inst = class_(**args)
		else:
			inst = d
		return inst


#class Person(object):
#	def __init__(self,name):
#		self.name = name
#	def __repr__(self):
#		return 'Person:name %s ' % self.name
#p = Person('zhangsan')
#d = MyEncoder().encode(p)
#o = MyDecoder().decode(d)
#print d
#print type(o),o
