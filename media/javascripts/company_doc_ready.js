function ready_map(id)
{
	initialize_company("map_" + id);
	
	base_coord = bases[id];
	opbase_routes = data[id];
	
	polys = []	
	
	/////////////////////////////////////////////////////////////////////

	if(opbase_routes != "None")
	{
		
		for(r in opbase_routes)			//each route (each poly line)
		{route = opbase_routes[r];
	
			polys.push(new GLatLng(base_coord[0],base_coord[1]));			//start the route at the base
		
			for(p in route)		//each point
			{point = route[p]
		
				polys.push(
			
					new GLatLng(point[0],point[1])
				);
			}
		
			polys.push(new GLatLng(base_coord[0],base_coord[1]));			//end the route at the base
		
			var polyline = new GPolyline(polys, "#ff0000", 3);
			maps["map_" + id].addOverlay(polyline);
		}
	}
	
	var marker_pos = new GLatLng(base_coord[0],base_coord[1]);			//a marker for the base
	
	var marker = new GMarker(marker_pos, icon);
	maps["map_" + id].addOverlay(marker);					//add the marker to the map
	
	polys.push(marker_pos);
	
	var latlngbounds = new GLatLngBounds( );

	for ( var i = 0; i < polys.length; i++ ){
		latlngbounds.extend( polys[ i ] );
	}
	
	maps["map_" + id].setCenter( latlngbounds.getCenter( ), maps["map_" + id].getBoundsZoomLevel( latlngbounds ) );
	
	if(polys.length == 1){			//if there are no lines, then set zoom to 6.
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

