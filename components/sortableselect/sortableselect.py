__pragma__("alias","s","$")
def sortable(widget_id,name):
	
	def update():
		
		def fn():
			value=""
			for elem in s(widget_id).find("li"):
				if s(elem).attr("data-value")!=None:
					if value!="":
						value+=","+s(elem).attr("data-value")
					else:
						value+=s(elem).attr("data-value")
			s("[name="+name+"]").val(value)
		setTimeout(fn,500)
		
		

	s(widget_id).sortable()
	s(widget_id).droppable({"drop":update})
	

	