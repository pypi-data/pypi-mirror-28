$(document).ready(function(){
	$("input[name='facturas_all']").on("click", sellect_all);
	$("#descargar_facturas_btn").hide();
	function sellect_all(){
		seleccionar = this.checked;

		$("input[type='checkbox'][name='facturas']").each(function(){
			this.checked = seleccionar;
		});
	}
	$("#descargar_facturas_btn").on("click", descargar_facturas);

	var progress = 0;
	var cliente_no_existe = ""
	var documento_ya_existe = ""
	var consecutivo_folio_no_definido = ""

	function descargar_facturas(){
		$("#certificar_facturas_btn, #descargar_facturas_btn").attr('disabled','disabled');
		$.ajax({
	 	   	url:'/enlace_liquida/descargar_facturas/',
	 	   	type : 'get',
	 	   	success: function(data){
	 	   		if (data.errors == ""){
	 	   			if (data.cliente_no_existe != "")
	 	   				cliente_no_existe = cliente_no_existe + ", "+data.cliente_no_existe;
	 	   			
	 	   			if (data.documento_ya_existe != "")
	 	   				documento_ya_existe = documento_ya_existe + ", "+data.documento_ya_existe;
	 	   			
	 	   			if (data.consecutivo_folio_no_definido != "")
	 	   				consecutivo_folio_no_definido = consecutivo_folio_no_definido + ", "+data.consecutivo_folio_no_definido;

		 	   		progress = data.progress;
		 	   		$("#progress-bar-unique").attr("aria-valuenow",progress);
		 	   		$("#progress-bar-unique").attr("style","width:"+progress+"%;");
		 	   		$("#progress-bar-unique").text(progress+"%, Factura de "+data.basedatos_no+ " generada.");
					if (progress < 100)
			 	   		descargar_facturas();
			 	   	else
			 	   	{
			 	   		var msg = "Facturas generadas."
			 	   		if (cliente_no_existe != "")
			 	   			msg = msg + "\n  Cliente no existe en \n["+ cliente_no_existe +"]";
			 	   		if (documento_ya_existe != "")
			 	   			msg = msg + "\n  Documento ya generado en \n["+ documento_ya_existe +"]";
			 	   		if (consecutivo_folio_no_definido != "")
			 	   			msg = msg + "\n  Consecutivo no definido en \n["+ consecutivo_folio_no_definido +"]";

			 	   		$("#certificar_facturas_btn, #descargar_facturas_btn").attr('disabled',false);
						alert(msg);
			 	   		window.location.href="/enlace_liquida/";
			 	   	}
	 	   		}
	 	   		else
	 	   			alert(data.errors);
	 	   	},	
	 	});	
	}

	$("#certificar_facturas_btn").on("click", certificar_facturas);
	
	var errores = "";
	var factura_selecionadas_obj = [];
	var facturas_certificadas="";
	var msg="";

	function certificar_facturas(){
		factura_selecionadas_obj  = $("input:checked[name='facturas']");

		if (factura_selecionadas_obj.length > 0) {
			$("#certificar_facturas_btn, #validar_empresas").attr('disabled','disabled');
			facturas_certificadas = ""
			errores = ""
			certificar_factura(0);
			msg="";
			
		}
		else{
			alert('Selecciona al menos una factura');
		};
	}

	function certificar_factura(index){
	  	/*Para tomar la factura a certificar*/
		valor_split = factura_selecionadas_obj[index].value.split(";");
		var using = valor_split[0];
		var factura_id = valor_split[1];

	  	$.ajax({
			url:'/enlace_liquida/certificar_factura/',
	 	   	type : 'get',
	 		data: {'factura_id':factura_id, 'using':using, },
	 		success: function(data){
	 	   		if (data.errors!= "")
		   			errores = errores + data.errors+"\n";
		   		else{
		   			facturas_certificadas = facturas_certificadas + using +",";	
		   		}
		   				
			},
			error: function (request, status, error) {
				   	errores=errores+using;
			},
			complete: function(request){
				var progress = (index +1 ) * 100 / factura_selecionadas_obj.length;
	 	   		progress=progress.toFixed(2);

		   		if (progress < 100){
					$("#progress-bar-unique").attr("aria-valuenow",progress);
			   		$("#progress-bar-unique").attr("style","width:"+progress+"%;");
			   		$("#progress-bar-unique").text(progress+"%, Certificando factura de "+using+ ".");
		   		}else{
		   			progress = 100;
		   			msg = msg +"\n Errores al certificar\n"+ errores+"\n";
		   			$("#progress-bar-unique").attr("aria-valuenow",progress);
		   			$("#progress-bar-unique").attr("style","width:"+progress+"%;");
		   			$("#progress-bar-unique").text(progress+"%, Base de datos ");
		   			
		   			if(facturas_certificadas.length>0){
		   				msg = msg+ "\nFacturas certificadas\n"+ facturas_certificadas;
		   				$("#certificar_facturas_btn, #validar_empresas").attr('disabled',false);
		   			};

		   			alert(msg);
		   			window.location.href="/enlace_liquida/";
		   		}
				
		   		certificar_factura(index+1);
			},
		});
	}
});