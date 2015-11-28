
$(document).on('ready', function() {
	$('.yelpImage').on('click', function(evt){ //when you click on .yelpImage class, this function runs
		var thingTheyClickedOn = evt.currentTarget;
		var latitude = $(thingTheyClickedOn).data('lat');
		var longitude = $(thingTheyClickedOn).data('long');
		console.log(thingTheyClickedOn)		//thingTheyClickedOn is the area where user can click within the yelpImage class
		var placeId = thingTheyClickedOn.id;
		console.log(placeId) // var placeId getting the ID of the place(rendered by jinja)
		var modalToShowId = 'modal' + placeId;//this variable is naming the modal adding the string "modal" and the id from YELP
		
		var modalMap = createMap(latitude, longitude, modalToShowId);
		
		$('#'+ modalToShowId).modal(); //jquery: the id(#) plus the modalToShow, make a modal

		$('#' + modalToShowId).find(".save-to-folder-button").on('click', function(e) {
			e.preventDefault();
			addPlaceToFolder(e.currentTarget, placeId);
		});
	
		google.maps.event.trigger(modalMap, 'resize');



	});
});

function createMap(latitude, longitude, modalToShowId){
	var mapLocation = $("#" + modalToShowId).find(".modal-map"); //the div for map. Different one for each modal2
	var LatLong = {lat: latitude, lng: longitude};
	var map = new google.maps.Map(mapLocation[0], 
	    {
	    	center: LatLong,
	    	zoom: 14,
	    	mapTypeId: google.maps.MapTypeId.ROADMAP,
	    }
	);
	var marker = new google.maps.Marker({
		position: LatLong,
		title: "Hi there!"
	});
	console.log(marker);

	marker.setMap(map);
	google.maps.event.addListenerOnce(map, 'idle', function() {
    	google.maps.event.trigger(map, 'resize');
	});

	google.maps.event.addListenerOnce(map, 'idle', function() {
		map.setCenter(LatLong);
    	
	});


	return map;
};



function addPlaceToFolder(folderElement, placeId) {
	var foldername = $(folderElement).text();
	var data = {"business_id": placeId,
				"folder_name": foldername};

	// debugger;

	$.post('/add-to-folder', data, function(response) {
		button.text("Remove");
		var wasAdded = response['added'];
		console.log("Got from the server: " + response);
	});
};




/////////////////// jQuery that submit a folder name to database and add the name to folder drop down //////////////////


$(document).on('ready', function(){
    //Handles menu drop down
    $('.folderform').submit(function(e) {
    	e.preventDefault();
    	var FolderName = $(e.currentTarget).find("input").val(); 
       	$.post('/new_folder', { 'FolderName' :  FolderName}, function(){
       	$(".add-folder-dropdown").hide();
       	$(".save-to-folder").append("<li class='save-to-folder-button'><a href='#'>"+FolderName+"</a></li>");
       	$(".list-of-folders").append("<li class='folders'><a href='#'>"+FolderName+"</a></li>");
       });
    });
});



/////////////////// JS function that automatically scroll up #results-section div upon SEARCH //////////////////

$(document).ready(function(){
    var result = $("#results-section");
    if (result.length>0){
    	$('html, body').animate({
        scrollTop: $("#results-section").offset().top
    	}, 500);
    }   
});



