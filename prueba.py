from .nuclear import Component,cloneElement
__pragma__("alias","s","$")
class Prueba(Component):
	"""
	"""
	def __init__(self):
		self.state={"bgColor":"red","text":"clonar boton","id":1}
	
	def clonar(self,evt):
		component=cloneElement(self)
		s(self.document).after(component.document)


	def cambiarColor(self):
		self.state.bgColor="blue"
		

	
	def render(self):
		return """
		<div>
			<label style="background:{{self.state.bgColor}}" > esto es un label de prueba</label>
			<button onclick={self.clonar(event)} style="background:"> {{self.state.text}} id: {{self.state.id}} </button>
			<button onclick={self.cambiarColor(event)} style=""> cambiar de color </button>
		</div>
		"""
