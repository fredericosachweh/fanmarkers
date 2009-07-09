function initialize()
{	
	if (GBrowserIsCompatible())
	{
		map = new GMap2(document.getElementById("map_canvas"));
		
		var polyOptions = {geodesic:true};
		
		map.addMapType(G_PHYSICAL_MAP);
		map.setMapType(G_PHYSICAL_MAP);
		
		map.setCenter(new GLatLng(10,0), 2);
		
		map.addControl(new GSmallZoomControl3D());
		map.addControl(new GHierarchicalMapTypeControl());
		map.enableContinuousZoom();
		map.enableScrollWheelZoom();
	}
}
