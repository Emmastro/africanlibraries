//Read - End Reading - Request reading feature

const nbrReads = $('#nbr-reads');
const API_ENDPOINT = "http://localhost:8000/api/";
const bookCard = $('#book');

const mainContent = $('[main-content]');
//const API_ENDPOINT


const initialise = () =>{
	
}

/*Search features*/

const searchFeature = () => {
	
	$('[search]').click(function(event) {
		//$("[name='key-search']").val("TEST");
		key = $("[name='key-search']").val();
		if (!key=='') {

		$.get('',
		{path:'search-by-key', key:key}, function (data, textStatus, jqXHR) {
			
			mainContent.empty();
			mainContent.append(data);
			
			//Hadle book clicks
			clickBook_eventHandler();
		});
	}
		
	});
}


const readAction_statut = () =>{
	/*Action for the 'read' button. */

	const readAction = $('#read-actions');
	const statut = readAction.attr('statut');

	if (statut==0) {
		readAction.text('Read');
	}
	else if (statut==1){
		readAction.text('End reading');

	}
	else if (statut==2){
		readAction.text('Request reading')
	}
	else{};

}


const eventHandler = () => {

}

showNotification = (from, align, type, message) => {
//type = ['', 'info', 'danger', 'success', 'warning', 'primary'];

$.notify({
  icon: "",
  message: message

}, {
  type: type,
  timer: 3000,
  placement: {
    from: from,
    align: align
  }
});
}


initialise(mainContent);
eventHandler();