$(document).ready(function() {
	

	$("#validar_empresas").on("click", validar_empresas);
	
	function validar_empresas(){
		$("#certificar_facturas_btn, #validar_empresas").attr('disabled','disabled');

		var empresas = [];
		var empresas_invalidas = [];
		var cliente_nombre = ''
		var articulo_nombre= ''
		var termino = false;
		var progress= 0;
		$.ajax({
	 	   	url:'/enlace_liquida/get_empresas_list/',
	 	   	type : 'get',
	 	   	success: function(data){
	 	   		empresas = data.empresas;
	 	   		cliente_nombre =  data.cliente_nombre;
	 	   		articulo_nombre = data.articulo_nombre;

	 	   		empresas.forEach(function(empresa, index){
 	   				$.ajax({
 	   			 	   	url:'/enlace_liquida/validar_empresa/',
 	   			 	   	type : 'get',
 	   			 		data: {'empresa_id':empresa, 'cliente_nombre':cliente_nombre, 'articulo_nombre':articulo_nombre, },
 	   			 	   	success: function(data){
 	   			 	   		if(data.is_valid ==  false){
 	   			 	   			empresas_invalidas.push(empresa);
 	   			 	   		}	

							progress = (index+1) * 100 / empresas.length;
							progress=progress.toFixed(2);

 	   			 	   		if (index==empresas.length-1) {
 	   			 	   			progress = 100;
 	   			 	   			$("#progress-bar-unique").attr("aria-valuenow",progress);
			 	   				$("#progress-bar-unique").attr("style","width:"+progress+"%;");
			 	   				$("#progress-bar-unique").text(progress+" %");

 	   			 	   			if (empresas_invalidas.length>0){
 	   			 	   				alert(":/ Empresas sin datos : \n "+empresas_invalidas);
 	   			 	   			}
 	   			 	   			else{
 	   			 	   				if( $("#descargar_facturas_btn").length==1){
 	   			 	   					$("#descargar_facturas_btn").show();
 	   			 	   					$("#validar_empresas").hide();
 	   			 	   				}
 	   			 	   				$("#certificar_facturas_btn, #validar_empresas").attr('disabled',false);
 	   			 	   				alert(":) Todas las empresas tienen los datos para facturar. ");
 	   			 	   			}
 	   			 	   		};

 	   			 	   		$("#progress-bar-unique").attr("aria-valuenow",progress);
		 	   				$("#progress-bar-unique").attr("style","width:"+progress+"%;");
		 	   				$("#progress-bar-unique").text(progress+" %");
							
 	   			 	   		
 	   					},
 	   				});
				});

				
			},
		});
	}



});



