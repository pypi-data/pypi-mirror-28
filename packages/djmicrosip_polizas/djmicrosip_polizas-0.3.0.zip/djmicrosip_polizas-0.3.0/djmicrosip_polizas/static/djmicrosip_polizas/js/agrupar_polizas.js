$("input[name='select_all']").on("click", sellect_all);
function sellect_all(){
	var to_select = this.checked;
	documentos = $("input[type='checkbox'][name='poliza']");
	documentos.each(function(){
		this.checked = to_select;
		mostrar_selecionados();
	});
}

function mostrar_selecionados(){
	var selecionados = $("input[type='checkbox'][name='poliza']:checked").length

	if (selecionados > 0) {
		$("#selected_documents_count").text(selecionados + " documentos selecionados.");
	}else{
		$("#selected_documents_count").text("");
	}
}

$("input[type='checkbox'][name='poliza']").on("click", mostrar_selecionados );

$("#btn_agrupar_polizas").on("click", function(){
	var documentos_selecionados = $("input[type='checkbox'][name='poliza']:checked").map(function() {return this.value;}).get();
	
	if (documentos_selecionados.length > 0) {
		$("#btn_agrupar_polizas").attr("disabled","disabled");
		debugger;
		$.ajax({
			url:'/polizas/polizas/agrupar_polizas_seleccionadas/', 
			type : 'get', 
			data:{
				'documentos':documentos_selecionados,
			}, 
			success: function(data){ 
				mensaje = ""
				if (data.num_documentos_procesados>0) {
					mensaje +=  data.num_documentos_procesados + " Polizas agrupadas, se agrego una descripción \n al final con 'POLIZA-AGRUPADA'";
				};

				alert(mensaje);
				location.reload(true);
			},
			error: function() {
				alert("fallo algo");
				$("#btn_agrupar_polizas").attr("disabled",false);
		  	},
		});

	}else{
		alert("Seleciona almenos un documento");
	}
});