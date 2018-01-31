function goBack() {
    window.history.back();
}

/*-------------------------------------------------------------------------
---------------------------------------------------------------------------
---------------------------------------------------------------------------
---------------------------------------------------------------------------
---------------------------------------------------------------------------*/
//index.html
/* Toggle between adding and removing the "responsive" class 
to topnav when the user clicks on the icon */
function toggle_menu() {
    var x = document.getElementById("myTopnav");
    if (x.className === "topnav") {
        x.className += " responsive";
    } else {        
        x.className = "topnav";
    }
} 

//Diccionario de "Departamentos" y "Municipios" creados en Python.
function setlist(val,elm_id)
{
		//Obtener indice del "Departamento" en el arreglo "cityLists (index.html)"
		var idx = val.selectedIndex;
		//Obtener arreglo de "Municipios" a partir del valor seleccionado
		var which = val.options[idx].value;
		cList = cityLists[which];//cityLists está definida en "index.html"

		var cSelect = document.getElementById(elm_id);
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
function setfields(val)
{
	cList = IPSLists[val];
	if (val!="")
	{					
		document.getElementById("ger").value=cList[0];
		document.getElementById("ger").text=cList[0];
		document.getElementById("nit").value=cList[1];
		document.getElementById("nit").text=cList[1];
		document.getElementById("car").value=cList[2];
		document.getElementById("tel").value=cList[3];
		document.getElementById("tel").text=cList[3];
		document.getElementById("Email").value=cList[4];
		document.getElementById("Email").text=cList[4];
		document.getElementById("addr").value=cList[5];
		document.getElementById("addr").text=cList[5];
		document.getElementById("username").value=cList[6];
		document.getElementById("username").text=cList[6];
		document.getElementById("usermail").value=cList[7];
		document.getElementById("usermail").text=cList[7];
		document.getElementById("userjob").value=cList[8];
		document.getElementById("userjob").text=cList[8];
		//document.getElementById("nivel".concat(cList[3])).checked=true;
	}
	else
	{				
		document.getElementById("nit").value='';
		document.getElementById("nit").text='';
		document.getElementById("car").value='';
		document.getElementById("ger").value='';
		document.getElementById("ger").text='';
		//document.getElementById("nivel1").checked=false;
		//document.getElementById("nivel2").checked=false;
		//document.getElementById("nivel3").checked=false;
		document.getElementById("tel").value='';
		document.getElementById("tel").text='';
		document.getElementById("Email").value='';
		document.getElementById("Email").text='';
		document.getElementById("addr").value='';
		document.getElementById("addr").text='';
		document.getElementById("username").value='';
		document.getElementById("username").text='';
		document.getElementById("usermail").value='';
		document.getElementById("usermail").text='';
		document.getElementById("userjob").value='';
		document.getElementById("userjob").text='';	
	}
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
