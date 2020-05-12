class path(object):
	"""docstring for path"""
	def __init__(self, pattern,view,name=None):
		super(path, self).__init__()
		self.pattern=pattern
class re_path(object):
	def __init__(self,pattern,view,name=None):
		super(re_path, self).__init__()
		self.pattern=pattern

		
class App(object):
	"""docstring for App"""
	urlpattern=[]
	def __init__(self):
		super(App, self).__init__()
		

	def loop(self):
		if "#" in location.href:
			url,path=location.href.split("#")


		pass
	def run(self):
		setTimeout(self.loop,0)

