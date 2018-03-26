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
	//document.getElementById("reg_numsede").value=IPSLists["Número de sedes"];
	//document.getElementById("reg_numsede").text=IPSLists["Número de sedes"];
	// document.getElementById("reg_nivel").value=IPSLists["Nivel del Prestador"];
	document.getElementById("reg_nit").value=IPSLists["NIT"];
	document.getElementById("reg_nit").text=IPSLists["NIT"];
	document.getElementById("reg_hab").value=IPSLists["Código Habilitación"];
	document.getElementById("reg_hab").text=IPSLists["Código Habilitación"];
	document.getElementById("reg_dptoP").value=IPSLists["Departamento"];//departamento-prestador
	setlist("reg_dptoP","reg_cityP")
	document.getElementById("reg_cityP").value=IPSLists["Municipio"];
	
	document.getElementById("reg_manag").value=IPSLists["Encargado de Encuesta"];
	document.getElementById("reg_manag").text=IPSLists["Encargado de Encuesta"];
	document.getElementById("reg_manmail").value=IPSLists["E-mail del Encargado"];
	document.getElementById("reg_manmail").text=IPSLists["E-mail del Encargado"];
	document.getElementById("reg_mantel").value=IPSLists["Teléfono del Encargado"];
	document.getElementById("reg_mantel").text=IPSLists["Teléfono del Encargado"];
}

/*-------------------------------------------------------------------------
---------------------------------------------------------------------------
---------------------------------------------------------------------------
---------------------------------------------------------------------------
---------------------------------------------------------------------------*/
//preguntas.html
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
