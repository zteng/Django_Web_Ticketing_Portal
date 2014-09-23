
function sendSearchByHostUniRequest() {
    $.ajax({
        type:"GET",
        url:"/search_by_hosting_university",
        data:{
            'csrfmiddlewaretoken':$('input[name=csrfmiddlewaretoken]').val(),
			'hostUni':$('select[name=hostUni]').val(),
        },
		//console.log('asdasd');
        success:handleSearchHostUniResponse,
		error:function(){
            alert("something went wrong");
        },
        dataType:'xml'
    });
}


function handleSearchHostUniResponse(xml){
	//alert("here");
    var node = document.getElementById("event_list");
    while (node.hasChildNodes()) {
       node.removeChild(node.firstChild);
    }
	// event info
	var info = $(xml).find('event_info')
	var events_num = $(info).find('events_num').text()
	content="";
	content = '<h3> Events <small class="pull-right" style="padding-top:20px">'+ events_num +' events are available </small></h3>'+	
			  '<hr class="soft"/>';
	content =content+ '<table class="table table-striped">'+
					  '<thead>'+
					  '<tr>'+
					  '<th>Date</th>'+
					  '<th>Match between</th>'+
					  '<th>Event Type</th>'+
					  '<th>Event Info</th>'+
					  '</tr>'+
					  '</thead>'+
					  '<tbody>';
    var items = $(xml).find('event');
    // Adds each new event-list item to the list
    for (var i = 0; i < items.length; ++i) {
    //    // Parses the item id and text from the DOM
        var event_date = $(items[i]).find("event_date").text()
        var event_time = $(items[i]).find("event_time").text()
        var event_host = $(items[i]).find("event_host").text()
        var event_away = $(items[i]).find("event_away").text()
        var event_type = $(items[i]).find("event_type").text()
		var event_cham = $(items[i]).find("event_cham").text()
		var event_id = $(items[i]).find("event_id").text()
		
        // Builds a new HTML list item for the todo-list item
        content = content+'<tr>'+
					      '<td style="width:20%">'+
						  '<p>'+event_date+'</p>'+
						  '<p>'+event_time+'</p>'+
						  '</td>'+
						  '<td style="width:25%">'+event_host+' <p style="margin-top:10px; color:red; font-size:20px">vs</p>'+ event_away+'</td>'+
						  '<td style="width:20%">'+event_type+'</td>'+
						  '<td style="width:35%">'+
						  '<p>'+event_cham+'</p>'+
						  '<a type="button" class="btn btn-info" href="/event/'+event_id+'">Detailed Info</a>'+
						  '</td>'+
						  '</tr>'
    }
	content = content+'</tbody>'+
					  '</table>	'+
					  '<hr>'
	node.innerHTML = content;
}

// causes the sendRequest function to run every 10 seconds
//window.setInterval(sendRequest, 10000);
