var CustomGetTileUrl = function(point,zoom){
	if ( zoom == 9 )	// Only retrieve a tile from the script on zoom level 9
		return "overlay_" + zoom + "_" + point.x + "_" + point.y + "_" + sessionKey;
	else
		return "overlay_0_0_0" ;	// Otherwise, use a blank image
}


var DestOverlay = new GTileLayerOverlay(
	new GTileLayer(null, null, null, {
		tileUrlTemplate: '/overlay_{Z}_{X}_{Y}_DMB/', 
		isPng:true,
		opacity:1.0
		}
	)
);

var BaseOverlay = new GTileLayerOverlay(
	new GTileLayer(null, null, null, {
		tileUrlTemplate: '/overlay_{Z}_{X}_{Y}_BMB/', 
		isPng:true,
		opacity:1.0
			}
	)
);



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
	}

	else if(map.getZoom() < 10){
		map.addOverlay(BaseOverlay);
		map.addOverlay(DestOverlay);
	}
	else{
	
		map.addOverlay(MarkerLayer);
	
	}
	
}

$(document).ready(function() {
		
	initialize();
	
});

window.onunload = GUnload;
