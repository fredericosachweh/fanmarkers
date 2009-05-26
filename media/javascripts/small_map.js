var icon = new GIcon;
	icon.image = "/site-media/icons/yellowdot.png";
	icon.iconSize = new GSize(16,16);
	icon.iconAnchor = new GPoint(8,8);
	icon.infoWindowAnchor = new GPoint(16,16);

var sicon = new GIcon;
	sicon.image = "/site-media/icons/smallblue.png";
	sicon.iconSize = new GSize(8,8);
	sicon.iconAnchor = new GPoint(4,4);
	sicon.infoWindowAnchor = new GPoint(8,8);
	
function initialize_airport()
{
	if (GBrowserIsCompatible())
	{
		map = new GMap2(document.getElementById("small_map"));
		
		map.setCenter(new GLatLng(airport_lat,airport_long), 6);
		
		map.addMapType(G_PHYSICAL_MAP);
		map.setMapType(G_PHYSICAL_MAP);
		
		map.addControl(new GSmallZoomControl3D());
		map.addControl(new GHierarchicalMapTypeControl());
		map.enableContinuousZoom();
		map.enableScrollWheelZoom();
		
		var marker = new GMarker(new GLatLng(airport_lat, airport_long), icon);
		map.addOverlay(marker);	

	}
}


function initialize_company(map_id)
{	
	if (GBrowserIsCompatible())
	{
		maps[map_id] = new GMap2(document.getElementById(map_id));
		
		var polyOptions = {geodesic:true};
		
		maps[map_id].addMapType(G_PHYSICAL_MAP);
		maps[map_id].setMapType(G_PHYSICAL_MAP);
		
		maps[map_id].addControl(new GSmallZoomControl3D());
		maps[map_id].addControl(new GHierarchicalMapTypeControl());
		maps[map_id].enableContinuousZoom();
		maps[map_id].enableScrollWheelZoom();
	}
}

function make_line(start_lat, start_long, end_lat, end_long, map_id)
{
	var polyOptions = {geodesic:true};
	var line = new GPolyline([new GLatLng(start_lat, start_long), new GLatLng(end_lat, end_long)], color, 2, 0.5, polyOptions);
	
	maps[map_id].addOverlay(line);
}
