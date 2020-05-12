from .nuclear import Component

class ChatBox(Component):
	"""docstring for ChatBox"""
	imports=[]
	presionadas=[]
	def __init__(self):
		self.state={"text":"","value":""}
	def keydown(self,evt):
		
		if evt.keyCode not in self.presionadas:
			self.presionadas.append(evt.keyCode)
		self.state.value=evt.currentTarget.value
	def keypress(self,evt):
		self.presionadas.sort()
		
		if str(self.presionadas) in str([13,17]):
			self.send()
	def drawResponse(self,data):
		node=document.createElement("DIV")
		
		if data["type"]=="text":
			console.log(document.querySelector("#hook-response"))
			self.hablar(data["response"])
			document.querySelector("#hook-response").innerHTML="""<pre
			style="
			    border: solid;
			    border-width: 2px;
			    border-radius: 50px 50px 50px 50px;
			    border-color: #5FA0FF;
			    position: absolute;
			    background: rgba(255,255,255,0.8);
			    right: -64px;
			    top: 0px;
			    display: inline-block;
			    width: 300px;
			    padding: 9px;
			    z-index: 1000;
			    overflow: auto;
			"
			>"""+data["response"]+"<pre>"

			
			document.querySelector("#hook-ctx").innerHTML=data["ctx"]
		elif data["type"]=="html":
			
			document.querySelector("#hook-response").innerHTML=data["response"]
			document.querySelector("#hook-ctx").innerHTML=data["ctx"]
			self.hablar(document.querySelector("#hook-response").innerText)

		location.href="#hook-response"

		
	def hablar(self,hablar,lang='es-ES'):
		if self.document.find("textarea").text().split()!="":
			self.send()

		if('speechSynthesis' in window):
		    speech =__new__(SpeechSynthesisUtterance)(hablar);
		    speech.lang = lang;
		    window.speechSynthesis.speak(speech);
	def llenarLista(self):
		def fn(dispositivos):
			limpiarSelect();
			def foreach(dispositivo, indice):
				if (dispositivo.kind == "audioinput"):
					opcion = document.createElement("option");
					# Firefox no trae nada con label, que viva la privacidad
					# y que muera la compatibilidad
					opcion.text = dispositivo.label or f"Dispositivo {indice + 1}";
					opcion.value = dispositivo.deviceId;
					listaDeDispositivos.appendChild(opcion);
                

			dispositivos.forEach(foreach)
            
		navigator\
        .mediaDevices\
        .enumerateDevices()\
        .then(fn)
            

		    
	def record(self):
		if (not listaDeDispositivos.options.length):
			return alert("No hay dispositivos");
		# No permitir que se grabe doblemente
		if (mediaRecorder): 
			return alert("Ya se está grabando");
		def fn(stream):
			#Comenzar a grabar con el stream
			self.mediaRecorder =__new__(MediaRecorder)(stream);
			self.mediaRecorder.start();
			comenzarAContar();
			#En el arreglo pondremos los datos que traiga el evento dataavailable
			fragmentosDeAudio = [];
			#Escuchar cuando haya datos disponibles
			self.mediaRecorder.addEventListener("dataavailable", lambda evento:fragmentosDeAudio.push(evento.data)# Y agregarlos a los fragmentos
              );
			#Cuando se detenga (haciendo click en el botón) se ejecuta esto
			def stop():
				#Detener el stream
			    stream.getTracks().forEach(lambda track: track.stop());
			    # Detener la cuenta regresiva
			    detenerConteo();
			    #Convertir los fragmentos a un objeto binario
			    blobAudio = __new__(Blob)(fragmentosDeAudio);

			    #Crear una URL o enlace para descargar
			    urlParaDescargar = URL.createObjectURL(blobAudio);
			    #Crear un elemento <a> invisible para descargar el audio
			    a = document.createElement("a");
			    document.body.appendChild(a);
			    a.style = "display: none";
			    a.href = urlParaDescargar;
			    a.download = "grabacion_parzibyte.me.webm";
			    #Hacer click en el enlace
			    a.click();
			    #Y remover el objeto
			    window.URL.revokeObjectURL(urlParaDescargar);
			self.mediaRecorder.addEventListener("stop", stop);


		navigator.mediaDevices.getUserMedia({
		          "audio": {
		              "deviceId": listaDeDispositivos.value,
		          }
		      })\
		      .then(fn)\
		      .catch(lambda error:console.log(error)#Aquí maneja el error, tal vez no dieron permiso
		      	);

	def stoprecord():
		self.mediaRecorder.stop()
	def segundosATiempo(numeroDeSegundos):
	    horas = Math.floor(numeroDeSegundos / 60 / 60);
	    numeroDeSegundos -= horas * 60 * 60;
	    minutos = Math.floor(numeroDeSegundos / 60);
	    numeroDeSegundos -= minutos * 60;
	    numeroDeSegundos = parseInt(numeroDeSegundos);
	    if (horas < 10):
	    	horas = "0" + horas;
	    if (minutos < 10):
	    	minutos = "0" + minutos;
	    if (numeroDeSegundos < 10):
	    	numeroDeSegundos = "0" + numeroDeSegundos;

	    return f"{horas}:{minutos}:{numeroDeSegundos}";


	#Ayudante para la duración; no ayuda en nada pero muestra algo informativo
	def comenzarAContar(self):
	    tiempoInicio = Date.now();
	    idIntervalo = setInterval(refrescar, 500);
	

	def refrescar(self):
	    duracion.textContent = segundosATiempo((Date.now() - tiempoInicio) / 1000);
	

		
		

	def send(self):
		
		fetch("/json/language/",{"method":"post",
							"body":JSON.stringify({
									"message":self.state.value})
						})\
		.then(lambda response:response.json()\
		.then(lambda json: self.drawResponse(json)))
	def send_message(self):
		if self.state.value!="":
			self.send()
		else:
			self.record()
		



	def keyup(self,evt):
		self.presionadas=[]

	def render(self):
		
		return """
		<div style="">
		{atajo}
		<div class="form-group" 
			style="display:flex;
				   flex-direction:row;
				   justify-content:center;
				   align-items:center;
			">
			
			<textarea onkeypress='{self.keypress(event)}' 
					  onkeydown='{self.keydown(event)}' 
					  onkeyup='{self.keyup(event)}' 

					  class="form-control" style="flex:1"></textarea>
		  <button 
		  class='btn-recognition' 
		  onclick="{self.send_message()}"
		  style="
		  flext:1;
		  background-image:url('/static/img/microfono.png');
		  background-repeat: no-repeat;
		  background-position: center;
		  background-size: 70%;
		  width:50px;
		  height:50px;
		  border-radius:50%;
		  background-color:#62A1F7;
		  border:solid;
		  border-width:1px;
		  "></button>
		 </div>
		 <input type="file">
		</div>
		""".format(atajo='<span style="margin-right:10px">Para enviar la consulta presiona Ctrl + Enter </span> ')
		