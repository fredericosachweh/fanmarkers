function initialize()
{
	if (GBrowserIsCompatible())
	{
		map = new GMap2(document.getElementById("map_canvas"));
		var polyOptions = {geodesic:true};
		
		var topLeft = new GControlPosition(G_ANCHOR_TOP_LEFT, new GSize(10,30));		//move the controls down so they are below the menu bar
		var topRight = new GControlPosition(G_ANCHOR_TOP_RIGHT, new GSize(10,30));
			
		map.setCenter(new GLatLng(10,0), 2);
		
		map.addMapType(G_PHYSICAL_MAP);
		map.setMapType(G_PHYSICAL_MAP);
		
		map.addControl(new GScaleControl());
		map.addControl(new GLargeMapControl3D(), topLeft);
		map.addControl(new GMapTypeControl(), topRight);
		map.enableContinuousZoom();
		map.enableScrollWheelZoom();
		
		africa = new GGeoXml('http://other.flightlogg.in/kml/africa.kmz');
		americas = new GGeoXml('http://other.flightlogg.in/kml/americas.kmz');
		carribean = new GGeoXml('http://other.flightlogg.in/kml/carribean.kmz');
		alaska = new GGeoXml('http://other.flightlogg.in/kml/alaska.kmz');
		austrailia = new GGeoXml('http://other.flightlogg.in/kml/austrailia.kmz');
		canada = new GGeoXml('http://other.flightlogg.in/kml/canada.kmz');
		china = new GGeoXml('http://other.flightlogg.in/kml/china.kmz');
		eastern_europe = new GGeoXml('http://other.flightlogg.in/kml/eastern_europe.kmz');
		europe = new GGeoXml('http://other.flightlogg.in/kml/europe.kmz');
		india = new GGeoXml('http://other.flightlogg.in/kml/india.kmz');
		indonesia = new GGeoXml('http://other.flightlogg.in/kml/indonesia.kmz');
		middle_east = new GGeoXml('http://other.flightlogg.in/kml/middle_east.kmz');
		russia = new GGeoXml('http://other.flightlogg.in/kml/russia.kmz');
		scandanavia = new GGeoXml('http://other.flightlogg.in/kml/scandanavia.kmz');
		usa = new GGeoXml('http://other.flightlogg.in/kml/usa.kmz');
		
		//map.addOverlay(africa);
		//map.addOverlay(americas);
		//map.addOverlay(carribean);
		//map.addOverlay(alaska);
		//map.addOverlay(austrailia);
		//map.addOverlay(canada);
		//map.addOverlay(china);
		//map.addOverlay(eastern_europe);
		//map.addOverlay(europe);
		//map.addOverlay(india);
		//map.addOverlay(indonesia);
		//map.addOverlay(middle_east);
		//map.addOverlay(russia);
		//map.addOverlay(scandanavia);
		//map.addOverlay(usa);
	}
}

window.onunload = GUnload;
