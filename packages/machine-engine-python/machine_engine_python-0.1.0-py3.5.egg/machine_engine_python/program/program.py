# from machine_engine_python import User

from machine_engine_python.user import User

class Program:


	def __init__(self, *args, **kwargs):

		# Default values
		self._id = None
		self.name = None
		self.type = None
		self.tags = []

		# Default structure
		self.user = None
		self.projects = []
		self.otherPrograms = []
		self.hubs = []

		self.combine(kwargs)

	def combine(self, *args, **kwargs):
		
		for key in kwargs:
			print("another keyword arg: %s: %s" % (key, kwargs[key]))

	def joke(self):
	    return (u'Wenn ist das Nunst\u00fcck git und Slotermeyer? Ja! ... '
	            u'Beiherhund das Oder die Flipperwaldt gersput.')
