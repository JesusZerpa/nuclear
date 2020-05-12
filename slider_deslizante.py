__pragma__("alias","array_from","Array.from")
c=0

class Slider(object):
	def __init__(self,
				selector,
				data={"velocity":1,
					  "direction":"left",
					  "orientation":"horizontal",
					  "width":"auto",
					  "height":"auto"}) -> Slider:
		if type(selector)==str:
			self.document=document.querySelectorAll(selector)
		elif NodeList.prototype.isPrototypeOf(selector):
			self.document=selector
		elif Node.prototype.isPrototypeOf(selector):
			self.document=[selector]
		else:
			self.document=selector
		self.maxdistance=0
		self.second_delay=0
		self.direction=data["direction"] if "direction" in data else "left"

		self.orientation=data["orientation"] if "orientation" in data else "horizontal"
		self.height=data["height"] if type(data["height"])==str else f"{data['height']}px"
		self.width=data["width"] if type(data["width"])==str else f"{data['width']}px"
		self.velocity=data["velocity"] if "velocity" in data else 1
		self.mode="prod"

		self.sliders={}
		
			

		
	def loop(self,slider):
		def fn(slider):			
			
			node=self.document[slider].querySelector(".slowslider-content")
			doc=self.sliders[slider]
			
			if not doc.paused:
				
				if self.direction=="left":
					
					node.scrollLeft+=1
					self.sliders[slider]["scrollleft"]=node.scrollLeft
					
					if node.scrollLeft>=self.sliders[slider]["maxdistance"]:
						node.scrollLeft=0
						self.sliders[slider]["scrollleft"]=node.scrollLeft
				elif self.direction=="right":
					node.scrollLeft-=1
					self.sliders[slider]["scrollleft"]=node.scrollLeft
					constante=35
					if node.scrollLeft<=((node.maxscroll*(self.sliders[slider]["maxdistance"]-node.offsetWidth))/node.scrollWidth)+constante:#35
						
						node.scrollLeft=node.scrollWidth
			self.sliders[slider]["control"]=False
		if not self.sliders[slider]["control"]:
			self.sliders[slider]["control"]=True
			setTimeout(lambda:fn(slider),self.sliders[slider]["second_delay"])
					
	def dragstart(self,evt):
		
		for k,elem in enumerate(self.document):
			found=True
			for slider in evt.path:
				if elem==slider:
					break
			else:
				found=False
			if found:
				break
		slider.x=evt.clientX
		slider.y=evt.clientY
		slider.paused=True
		
		
	def drag(self,evt):

		for k,elem in enumerate(self.document):
			found=True
			for slider in evt.path:
				if elem==slider:
					break
			else:
				found=False
			if found:
				break
		
		
		
		
		dx=evt.clientX-slider.x
		dy=evt.clientY-slider.y
		slider.x=evt.clientX
		slider.y=evt.clientY
		slider.paused=True
		if self.orientation=="horizontal":
			slider.querySelector(".slowslider-content").scrollLeft+=dx
			self.sliders[k]["scrollleft"]=slider.querySelector(".slowslider-content").scrollLeft
			#slider.scrollleft=self.sliders[k]["scrollleft"]
		elif self.orientation=="vertical":
			slider.querySelector(".slowslider-content").scrollTop+=dy
			#slider.scrollltop=self.slider[k]["scrolltop"]
		


	def dragend(self,evt):
		
		for k,elem in enumerate(self.document):
			found=True
			for slider in evt.path:
				if elem==slider:
					break
			else:
				found=False
			if found:
				break
		
		
		
		slider.querySelector(".slowslider-content").scrollLeft=self.sliders[k]["scrollleft"]
		
		slider.paused=False
	def mouseover(self,evt):
		
		for k,elem in enumerate(self.document):
			found=True
			for slider in evt.path:
				if elem==slider:
					break
			else:
				found=False
			if found:
				break
		
		#slider.paused=True
		self.sliders[k]["second_delay"]=50
	def mouseout(self,evt):
		
		for k,elem in enumerate(self.document):
			found=True
			for slider in evt.path:
				if elem==slider:
					break
			else:
				found=False
			if found:
				break

		#slider.paused=False
		self.sliders[k]["second_delay"]=0
		
				
	def recursive(self,node,fn):
		
		for node in node.children:
			fn(node)
			self.recursive(node,fn)
		


	def reload(self):
		
		for k,doc in enumerate(self.document):
			node=doc.querySelector("[data-height]")
			if node!=None:
				self.height=node.attributes["data-height"].value
				if "data-velocity" in node.attributes:
					self.velocity=int(node.attributes["data-velocity"].value.replace("px",""))
				if "data-width" in node.attributes:
					self.width=node.attributes["data-width"].value
				if "data-direction" in node.attributes:
					self.direction=node.attributes["data-direction"].value
				if "data-orientation" in node.attributes:
					self.orientation=node.attributes["data-orientation"].value
			
			#self.recursive(doc,lambda node: setattr(node.style,"maxHeight",self.height))
			clones=[]
			doc.maxdistance=0
			children=doc.querySelector(".slowslider-content").children
			for node in children:
				if "data-clone" in node.attributes:
					node.remove()
			children=doc.querySelector(".slowslider-content").children
			for node in children:
				clones.append(node.cloneNode(True))
				self.sliders[k]["maxdistance"]+=node.offsetWidth	
			for node in clones:
				node.setAttribute("data-clone",True)
				doc.querySelector(".slowslider-content").appendChild(node)
		
	

	def run(self):
		
		for k,doc in enumerate(self.document):
			doc.setAttribute("draggable",True)
			doc.paused=False
			if "slider" in dir(doc):
				clearInterval(doc.sider.mainloop)
				del doc.slider
			#doc.addEventListener("dragstart",self.dragstart)
			#doc.addEventListener("drag",self.drag)
			#doc.addEventListener("dragend",self.dragend)
			doc.addEventListener("mouseover",self.mouseover)
			doc.addEventListener("mouseout",self.mouseout)
			self.sliders[k]={}
			self.sliders[k]["scrollleft"]=0
			self.sliders[k]["scrolltop"]=0
			self.sliders[k]["second_delay"]=0
			self.sliders[k]["control"]=False
			self.sliders[k]["maxdistance"]=0
			doc.slider=self
			node=doc.querySelector(".slowslider-content")
			if self.mode=="prod":
				node.style.overflow="hidden"		
			elif self.mode=="edit":
				node.style.overflow="scroll"		
			if self.orientation=="horizontal":
				node.style.flexDirection="row";
			elif self.orientation=="vertical":
				node.style.flexDirection="column";
				node.style.height=height;
			
			node.style.height=self.height;
			node.style.width=self.width;

			node.style.display="flex";
			node.style.flexDirection="row";
			
			self.reload()
			if self.direction=="right":
				node.scrollLeft=node.scrollWidth
				self.sliders[k]["maxdistance"]+=node.offsetWidth

			self.maxscroll=node.scrollLeft
			if self.mode=="prod":
				doc.mainloop=setInterval(lambda: self.loop(k),self.velocity)
	
		





