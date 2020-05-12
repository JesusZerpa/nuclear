__pragma__("alias","s","$")

window.nuclear_app=None
pattern=r"(\{\{.*?\}\})"

class State(object):
	"""docstring for Prop"""
	def __init__(self,prop={}):
		self.prop=prop
		self.component=None
	def __getattr__(self,key):
		return self.prop[key]

	def __setattr__(self,key,value):
		
		self.prop[key]=value		
		self.component.refresh()

class Prop(object):
	"""docstring for Prop"""
	
	component=None	
	def __getattr__(self,key,otracosa):
		console.log(key,self,otracosa)

		return self.component.document.getAttribute(key)
	def __getitem__(self,key,otracosa):
		
		return self.component.document.getAttribute(key)

def addMethod(node,self=None):
	"""
	Pareciera que toma los componentes desde el html y los componentes
	que tiene listados que sabe que usara en imports
	"""
	hasoriginal=False
	#lectura
	
	if self.root!=None and node.nodeName in self.root.imports_names:

		if node.self==None:

			i=self.root.imports_names.index(node.nodeName)

			_self=self.root.imports[i]()
			self.children.append(_self)
			_self.parent=self

			self.root.components.append(_self)
			_self.root=self.root
			node.self=_self
			_self.document=node
			_self.draw()
			_self.refresh()



	else:
		
		if node.nodeName!="#text":
			if node.self==None:

				node.self=self


			
			
			if node.originalAttr==None and node.self.is_clone==None:
				node.originalAttr={}
			elif node.originalAttr==None and node.self.is_clone!=None:
				node.originalAttr=node.originalNode.originalAttr
		
			for attr in node.getAttributeNames():
				
				if attr.startswith("on"):
					val=node.getAttribute(attr)
					
					if node.self.is_clone==None:
						if val.startswith("{") and val.endswith("}"):
							val="{var self=this.self;"+val+"}"
						
						node.setAttribute(attr,val)
				else:

					if not len(node.originalAttr.keys()):
						val=node.getAttribute(attr)
					else:
						
						val=node.originalAttr[attr]

					if "{{" in val and "}}" in val:
						node.originalAttr[attr]=val
						if node.self!=None:

 							if node not in node.self.listener_nodes: 								
 								node.self.listener_nodes.append(node)

 								

						

		elif node.nodeName=="#text":

			if node.self==None:
				node.self=self
				if "{{" in node.nodeValue and "}}" in node.nodeValue:
					node.orginalValue=node.nodeValue
				
					if node.self!=None:
						if node not in node.self.listener_nodes:

							node.self.listener_nodes.append(node)
							

		
	
	for elem in node.childNodes: 			 						
		addMethod(elem,self)

class Component(object):
	"""docstring for Component"""
	imports=[]
	imports_names=[]
	is_root=False
	root=None
	selector=None
	_state={}
	listener_nodes=[]
	components=[]
	children=[]
	navigationOtions=None
	panels=[]#son como las diferentes instancias de apps que estan en la pantalla pero se integran aqui a un control principal
	def __init__(self):
		self.props=Prop()
		self.props.component=self
	@property
	def state(self):
		return self._state

	@state.setter
	def state(self,value):
		p=State(value)

		p.component=self
		self._state=p
		
		#self.refresh()
	def synChanges(self,event,attr):
		
		setattr(self.state,attr,event.currentTarget.value)

	def mount(self):
		"""
		cuando el componente se monta
		"""
	def dismount(self):
		"""
		Cuando el componente se desmonta (se elimina)
		"""


	def refresh(self):
		
		for node in self.listener_nodes:

			self.refreshAttr(node)
			self.refreshText(node)



		
	def render(self):
		if self.selector!=None:
			return document.querySelector(self.selector).innerHTML
		else:
			return f"<pre> Debes definir un renderizado para el componente{self.__class__.__name__}</pre>"
		
	def refreshAttr(self,node):
		
		if self==node.self:

			if node.nodeName!="#text":
				
				re=__new__(RegExp(pattern,"mg"))

				for attr in node.originalAttr.keys():
					val=node.getAttribute(attr)
					
					matches=node.originalAttr[attr].match(re)
					
					if matches:
						for match in matches:	
							
							tag=node.originalAttr[attr].replace(match,eval(match.slice(2,-2)))
							

							node.setAttribute(attr,tag)
					
			

	def refreshText(self,node):
		"""
		esto se hace porque de alguna los nodos se agregan a los otros components
		por lo que hay que compararla con su self para que no se refresque
		"""
		if self==node.self:
			

			if node.nodeName=="#text":
				val=node.orginalValue
				
				re=__new__(RegExp(pattern,"mg"))
				matches=val.match(re)
				
				if matches:
					for match in matches:
						val=val.replace(match,eval(match.slice(2,-2)))
						node.nodeValue=val

	
	def _connect(self):

		for elem in self.document.childNodes:
			addMethod(elem,self)

	def draw(self):	
		self.document.innerHTML=self.render()

		self._connect()
		
		self.refresh()

	def render_panel(self,selector=None):
		"""
		aqui selector indica que puedes colocar el panel en otro selector
		diferente al selector que usastes como plantilla, si es que usastes 
		una
		"""
		if selector==None:
			selector=self.selector	
		if selector!=None:
			self.document=document.querySelector(selector)
			self.render()
			self.draw()
		else:
			print("Debes indicar un selector donde colocar el panel")



		



def render(app,id):
	
	instancia=app()
	instancia.panels
	instancia.is_root=True
	window.nuclear_app=instancia
	pattron=r"/(\w+)\=(\{.*?\}.*?\})/"
	imports=[]

	def importar(node):

		for elem in node.imports:
			if elem not in imports:
				imports.append(elem)
				instancia.imports_names.append(elem.__name__.upper())
				importar(elem)

	for elem in instancia.imports:
		imports.append(elem)
		instancia.imports_names.append(elem.__name__.upper())
		importar(elem)
		
	instancia.imports=imports

	def fn2(node):
		
		if node.nodeName in instancia.imports_names:
			
			if node.self==None:
				i=instancia.imports_names.index(node.nodeName)
				self=instancia.imports[i]()

				self.children.append(self)
				self.root=instancia
				node.self=self
				self.document=node				
				self.draw()

			
		[fn2(_node) for _node in node.childNodes]
	root=document.querySelector("#"+id)
	doc=instancia.render()
	console.log(doc)
	root.innerHTML=doc
	console.log(root.innerHTML)


	
	

	[fn2(_node) for _node in root.childNodes]


	
	
	
	
	
def forChildNodes(node,fn):
	fn(node)
	node.ChildNodes.forEach(fn)
def makeclone(node,original=None):
	if original==None:
		
		elem=node.cloneNode(False)
		elem.originalNode=node
		for hijo in node.childNodes:
			makeclone(elem,hijo)
		return elem
	else:
		#aqui node es el padre clonado 
		elem=original.cloneNode(False)
		elem.originalNode=original
		node.appendChild(elem)
		for hijo in original.childNodes:
			makeclone(elem,hijo)

def cloneElement(component,props):
	for k,elem in enumerate(component.root.imports):
		if elem.__name__==component.__class__.__name__:
			clon=elem()
			elem.parent.children.append(clon)
			clon.parent=elem.parent
			clon.is_clone=True
			clon.root=component.root
			clon.document=makeclone(component.document)
			clon.document.self=clon			
			for node in clon.document.childNodes:
				addMethod(clon.document,clon)



	return clon
	
class Navigation(object):
	history=[]
	getParam=None
	routes={}
	def __init__(self,routes,navigationOtions):
		setInterval(self.change,100)

	def goback(self):
		self.location.hef=history[-1]
	def push(self,route):
		component=self.routes[route]()
		component.document=document.createElement(component.__class__.__name__)
		component.draw()
	def setParams(self,params):
		pass
	def change(self):
		url=self.location.href.split("#")
		if len(url)==2:
			params=url[1].split("?")
			if len(params)==2:
				self.getParam=__new__(URLSearchParams)(params[1])



				
	
def createAppContainer(navigator):
	pass
