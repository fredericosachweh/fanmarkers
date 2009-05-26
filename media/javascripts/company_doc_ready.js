function ready_map(id)
{
	initialize_company("map_" + id);				//id = the pk of the current opbase
	
	base_coord = bases[id];
	opbase_routes = data[id];
	
	route_points = [];			//contains the points of each route; cleared after each route
	all_points = []			//contains the points of all routes per opbase
	small_points = [];
	
	/////////////////////////////////////////////////////////////////////

	if(opbase_routes != "None")
	{
		
		for(r in opbase_routes)			//each route (each poly line)
		{route = opbase_routes[r];
	
			route_points.push(new GLatLng(base_coord[0],base_coord[1]));			//start the route at the base
		
			for(p in route)		//each point
			{point = route[p]
		
				route_points.push(new GLatLng(point[0],point[1]));
				small_points.push(new GLatLng(point[0],point[1]));
				all_points.push(new GLatLng(point[0],point[1]));
			}
		
			route_points.push(new GLatLng(base_coord[0],base_coord[1]));			//end the route at the base
		
			var polyline = new GPolyline(route_points, "#ff0000", 3);
			maps["map_" + id].addOverlay(polyline);
			
			route_points = [];							//clears for the next route
		}
	}
	
	var marker = new GMarker(new GLatLng(base_coord[0],base_coord[1]), icon);
	maps["map_" + id].addOverlay(marker);							//add the marker for the base
	
	all_points.push(new GLatLng(base_coord[0],base_coord[1]));
	
	for(p in small_points)									//make the small dots on each stop
	{this_point = small_points[p];
			
		var marker = new GMarker(this_point, sicon);
		maps["map_" + id].addOverlay(marker);
	}
	
	///////// find the map center
	
	var latlngbounds = new GLatLngBounds( );
	for ( var i = 0; i < all_points.length; i++ ){
		latlngbounds.extend( all_points[ i ] );
	}
	maps["map_" + id].setCenter( latlngbounds.getCenter( ), maps["map_" + id].getBoundsZoomLevel( latlngbounds ) );
	
	//////// set the map zoom
	
	if(all_points.length == 1){							//if there are no lines, then set zoom to 6.
		maps["map_" + id].setZoom(6)
	}
}

$(document).ready(function() {

	$("a[href=]").click(function(event) {			//all fake anchors are disabled
		event.preventDefault();
	});

	$(".plus").click(function plusclick(){
	
		id_num = this.id.substr(7);
		plusclick.done = [];				//function is an object, properties act like static variables
		
		$("#info_" + id_num).toggle('fast');
		
		if($("#expand_" + id_num).attr('src') == '/site-media/plus.png'){
			$("#expand_" + id_num).attr('src', '/site-media/minus.png');
			if(!plusclick.done[id_num]){
				ready_map(id_num);
				plusclick.done[id_num] = true;			//record this function being ran so the map isnt initialized twice
			}
		}
		else	$("#expand_" + id_num).attr('src', '/site-media/plus.png');
	});	

});		

