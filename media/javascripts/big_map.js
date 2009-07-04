var CustomGetTileUrl = function(point,zoom){
	if ( zoom == 9 )	// Only retrieve a tile from the script on zoom level 9
		return "overlay_" + zoom + "_" + point.x + "_" + point.y + "_" + sessionKey;
	else
		return "overlay_0_0_0" ;	// Otherwise, use a blank image
}


var BaseOverlay = new GTileLayerOverlay(
	new GTileLayer(null, null, null, {
		tileUrlTemplate: '/overlay/{Z}_{X}_{Y}_DMB/', 
		isPng:true,
		opacity:1.0
		}
	)
);

var offset = new GSize(-17,10)

var labels =
	[	
		new ELabel(new GLatLng(10.885097,20.361325), "38", "overlay_number", offset),		// africa
		new ELabel(new GLatLng(-13.137258, -59.824226), "38", "overlay_number", offset),	// americas
		new ELabel(new GLatLng(18.746149, -71.777351), "38", "overlay_number", offset),		// carribean
		new ELabel(new GLatLng(65.315500, -153.662113), "38", "overlay_number", offset),	// alaska
		new ELabel(new GLatLng(-25.593975,138.837887), "38", "overlay_number", offset),		// australia
		new ELabel(new GLatLng(59.471873,-103.037113), "38", "overlay_number", offset),		// canada
		new ELabel(new GLatLng(34.328693,100.869137), "38", "overlay_number", offset),		// china
		new ELabel(new GLatLng(49.187448,27.919918), "38", "overlay_number", offset),		// east-europe
		new ELabel(new GLatLng(49.644869,1.419918), "38", "overlay_number", offset),		// europe
		new ELabel(new GLatLng(24.415142,78.7207), "38", "overlay_number", offset),		// india
		new ELabel(new GLatLng(1.810246,113.87695), "38", "overlay_number", offset),		// indonesia
		new ELabel(new GLatLng(28.659744,49.716793), "38", "overlay_number", offset),		// middle-east
		new ELabel(new GLatLng(65.3155,82.412106), "38", "overlay_number", offset),		// russia
		new ELabel(new GLatLng(67.960532,20.712887), "38", "overlay_number", offset),		// scandanavia
		new ELabel(new GLatLng(39.524382, -98.100588), "38", "overlay_number", offset),		// usa		
	]
	

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
		
		figure_zoom();
		
		GEvent.addListener(map, "zoomend", figure_zoom);
	}
}

function figure_zoom()
{	
	map.clearOverlays();
	
	if(map.getZoom() < 3 ){
		map.addOverlay(africa);
		map.addOverlay(americas);
		map.addOverlay(carribean);
		map.addOverlay(alaska);
		map.addOverlay(austrailia);
		map.addOverlay(canada);
		map.addOverlay(china);
		map.addOverlay(eastern_europe);
		map.addOverlay(europe);
		map.addOverlay(india);
		map.addOverlay(indonesia);
		map.addOverlay(middle_east);
		map.addOverlay(russia);
		map.addOverlay(scandanavia);
		map.addOverlay(usa);
		
		for(item in labels)
		{
			map.addOverlay(labels[item]);
		}
	}

	else if(map.getZoom() < 10){
		map.addOverlay(BaseOverlay);
	}
	else{
		map.addOverlay(MarkerLayer);
	}
	
}

$(document).ready(function() {
		
	initialize();
	
});

window.onunload = GUnload;
