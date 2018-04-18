function goBack() {
    window.history.back();
}

/*Alertas*/
function alerta(msg) {
    alert(msg);
}

function logval() {
	if (LogVal=="True")
	{
		document.getElementById("vallog").text="\u26DD  Cerrar sesión";
		document.getElementById("vallog").setAttribute("href","/logout")
	}
	else{
		document.getElementById("vallog").value="\u26BF Ingresar";
		document.getElementById("vallog").setAttribute("href","/Ingresar")
	}

}


/*-------------------------------------------------------------------------
---------------------------------------------------------------------------
---------------------------------------------------------------------------
---------------------------------------------------------------------------
---------------------------------------------------------------------------*/
//index.html
/* Toggle between adding and removing the "responsive" class 
to topnav when the user clicks on the icon */
function toggle_menu(barid) {
    var x = document.getElementById(barid);
    if (x.className === "topnav") {
		x.className += " responsive";		
		document.getElementById("icon").text="\u26DD";
    } else {        
		x.className = "topnav";		
		document.getElementById("icon").text="\u2630";
    }
} 

//Diccionario de "Departamentos" y "Municipios" creados en Python.
function setlist(dpto_id,city_id)
{		
		//Obtener indice del "Departamento" en el arreglo "cityLists (registro.html)"
		//var idx = val.selectedIndex;
		//Obtener arreglo de "Municipios" a partir del valor seleccionado
		//var which = val.options[idx].value;
		//cList = cityLists[which];//cityLists está definida en "registro.html"
		val = document.getElementById(dpto_id).value
		cList = cityLists[val];//cityLists está definida en "registro.html"		
		var cSelect = document.getElementById(city_id);
		var len = cSelect.options.length;
		while (cSelect.options.length > 0) {
		cSelect.remove(0);
		}

		//Crear lista de cuidades
		var newOption;
		//Crear opción por defecto
		newOption = document.createElement("option");
		newOption.value = "";
		newOption.text = "Seleccionar";
		try
			{
				cSelect.add(newOption);  //this will fail in DOM browsers but is needed for IE
			}
		catch (e)
			{
				cSelect.appendChild(newOption);
			}
		//Crear lista de municipios
		for (var i=0; i<cList.length; i++)
		{
			newOption = document.createElement("option");
			newOption.value = cList[i];
			newOption.text = cList[i];

			try
			{
				cSelect.add(newOption);  //this will fail in DOM browsers but is needed for IE
			}
			catch (e)
			{
				cSelect.appendChild(newOption);
			}
		}
}

/*-------------------------------------------------------------------------
---------------------------------------------------------------------------
---------------------------------------------------------------------------
---------------------------------------------------------------------------
---------------------------------------------------------------------------*/
//registro.html; DB_IPS.py; forms.py
//Esta función se utiliza para autcompletar datos de registro en 
//caso de que la IPS se encuentre en la base de datos.
function setfields()
{
	document.getElementById("reg_ips").value=IPSLists["Nombre del Prestador"];
	document.getElementById("reg_ips").text=IPSLists["Nombre del Prestador"];
	document.getElementById("reg_numsede").value=IPSLists["Número de sede"];
	document.getElementById("reg_numsede").text=IPSLists["Número de sede"];
	// document.getElementById("reg_nivel").value=IPSLists["Nivel del Prestador"];
	document.getElementById("reg_nit").value=IPSLists["NIT"];
	document.getElementById("reg_nit").text=IPSLists["NIT"];
	document.getElementById("reg_hab").value=IPSLists["Código Habilitación"];
	document.getElementById("reg_hab").text=IPSLists["Código Habilitación"];
	document.getElementById("reg_codcity").value=IPSLists["Código Municipio"];
	document.getElementById("reg_codcity").text=IPSLists["Código Municipio"];
	document.getElementById("reg_coddpto").value=IPSLists["Código Departamento"];
	document.getElementById("reg_coddpto").text=IPSLists["Código Departamento"];
	document.getElementById("reg_manag").value=IPSLists["Encargado de Encuesta"];
	document.getElementById("reg_manag").text=IPSLists["Encargado de Encuesta"];
	document.getElementById("reg_manmail").value=IPSLists["E-mail del Encargado"];
	document.getElementById("reg_manmail").text=IPSLists["E-mail del Encargado"];
	document.getElementById("reg_mantel").value=IPSLists["Teléfono del Encargado"];
	document.getElementById("reg_mantel").text=IPSLists["Teléfono del Encargado"];
	document.getElementById("reg_dptoP").value=IPSLists["Departamento"];//departamento-prestador
	setlist("reg_dptoP","reg_cityP")
	document.getElementById("reg_cityP").value=IPSLists["Municipio"];	
}

/*-------------------------------------------------------------------------
---------------------------------------------------------------------------
---------------------------------------------------------------------------
---------------------------------------------------------------------------
---------------------------------------------------------------------------*/
//preguntas.html
//Cargar respuestas tipo radio
function set_radios(x,val)
{
	var radio = x[i].value;
	if (radio.localeCompare(val)==0)
	{	
		var temp = x[i].id

		document.getElementById(x[i].id).checked = true;//MARCAR respuesta
		if (temp.search('_hab')!=-1)//Para disparar eventos que habilitan otras opciones
		{
			$(document.getElementById(x[i].id)).click();			
		}
	}
}
//marcar respuestas tipo checkbox
function set_checkbox(x,val)
{
	for( j = 0; j < val.length; j++ ) 
	{
		var check = x.value;
		if (check.localeCompare(val[j])==0)
		{	
			document.getElementById(x.id).checked = true;	
		}
	}
}
//Marcar preguntas contestadas
function set_rtas()
{
	for(var key in Rtas)
	{
		if (key.localeCompare('ID')!=0)
		{
			var x = document.getElementsByName(key);
			var val = Rtas[key];			
			for( i = 0; i < x.length; i++ ) 
			{				
				var elem = x[i].type	
				if (elem.localeCompare('radio')==0)
				{
					set_radios(x,val);
				}
				if (elem.localeCompare('checkbox')==0)
				{
					set_checkbox(x[i],val);
				}
				if (elem.localeCompare('number')==0)
				{
					document.getElementById(x[i].id).value = val;
				}
				if (elem.localeCompare('text')==0)
				{
					document.getElementById(x[i].id).value = val;
					document.getElementById(x[i].id).text = val;
				}
			}
		}
	}
	
}
//obtener elementos contenidos en una clase
function clear_inputs(classcont)
{
	var c = document.getElementById(classcont).querySelectorAll('*');//Obtener todos los elementos de una clase
	for (i = 0; i < c.length; i++) 
	{
		var temp = c[i].nodeName;//Verificar que sea entrada
		if (temp.localeCompare('INPUT')==0)
		{
			var elem = c[i].type//Verificar el tipo de entrada
			if (elem.localeCompare('radio')==0)
			{
				c[i].checked=false;
			}
			if (elem.localeCompare('checkbox')==0)
			{
				c[i].checked=false;
			}			
			if (elem.localeCompare('number')==0)
			{
				c[i].value=0;
			}
			if (elem.localeCompare('text')==0)
			{
				c[i].text='';
			}
		}
    }
}
//Mostrar opcion para borrar adjunto
function enb_dis(btn_att,btn_del)
{
	var x = document.getElementById(btn_att);
	var input = document.getElementById(btn_del);
	if ('files' in x)
	{
	   input.disabled = false;
	   input.focus();
	}
	else
	{
	   input.disabled = true;
	}
}
//Borrar archivo adjunto
function delete_attached(btn_del,name)
{
	document.getElementById(name).value = "";
	document.getElementById(btn_del).disabled = true;
}

//solo texto, espacios, y guiones
function textonly(e){
	var code;
	if (!e) var e = window.event;
	if (e.keyCode) code = e.keyCode;
	else if (e.which) code = e.which;
	var character = String.fromCharCode(code);
	var AllowRegex  = /^[\ba-zA-Z\s-]$/;
	if (AllowRegex.test(character)) return true;    
	return false;
	}

// Activar contenedores
function yesnoCheck(questionIDYesNO, questionIDYes, questionIDNO) 
{
	if (questionIDYesNO.checked) 
	{
	$(questionIDYes).removeClass("hidden");
	$(questionIDNO).addClass("hidden");
	}
}
// activar a partir de checkboxes
function Checkb(obj,containerid) 
{
	if (obj.checked)//Mostrar
	{
	$(containerid).removeClass("hidden");
	}
	else//Ocultar
	{
	$(containerid).addClass("hidden");
	}
}

// activar entrada de texto OTROS
function inputOn(obj,textInput)
{
	var input=document.getElementById(textInput); 
	if(obj.checked)
	{ 
		input.disabled = false; 
		input.focus();
	}
	else
	{
		input.value='';
		input.disabled=true;
	}
}


	// Deshabilitar con Radio
function disradio(radObj)
{
	document.getElementById(radObj).disabled=true;
	document.getElementById(radObj).value='';
}

