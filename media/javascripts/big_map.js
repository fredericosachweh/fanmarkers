var CustomGetTileUrl = function(point,zoom){
	if ( zoom == 9 )	// Only retrieve a tile from the script on zoom level 9
		return "overlay_" + zoom + "_" + point.x + "_" + point.y + "_" + sessionKey;
	else
		return "overlay_0_0_0" ;	// Otherwise, use a blank image
}


var BaseOverlay = new GTileLayerOverlay(
	new GTileLayer(null, null, null, {
		tileUrlTemplate: '/overlay/{Z}_{X}_{Y}_DMB.png', 
		isPng:true,
		opacity:1.0
		}
	)
);

var offset = new GSize(-17,20)
var instructions = "<b>Top Number</b>: Total Hiring Positions<br><br><b>Bottom Number</b>: Total Positions<br><br><b>Zoom in for more detail</b><br><br><i>**Many Features of this site are currently not implemented in Opera and especially IE. For best results, use Firefox 3.5 or Google Chrome**</i><br><br>Register an account to edit information and create new Company/Position/Aircraft profiles.";

var labels =
	[	
		new ELabel(new GLatLng(10.885097,20.361325),  africa[1] + "<br>" + africa[2], "overlay_number", offset),		// africa
		new ELabel(new GLatLng(-13.137258,-59.824226), americas[1] + "<br>" + americas[2], "overlay_number", offset),		// americas
		new ELabel(new GLatLng(18.746149,-71.777351), carribean[1] + "<br>" + carribean[2], "overlay_number", offset),		// carribean
		new ELabel(new GLatLng(65.315500,-153.662113), alaska[1] + "<br>" + alaska[2], "overlay_number", offset),		// alaska
		new ELabel(new GLatLng(-25.593975,138.837887), australia[1] + "<br>" + australia[2], "overlay_number", offset),		// australia
		new ELabel(new GLatLng(59.471873,-103.037113),  canada[1] + "<br>" + canada[2], "overlay_number", offset),		// canada
		new ELabel(new GLatLng(34.328693,100.869137), china[1] + "<br>" + china[2], "overlay_number", offset),			// china
		new ELabel(new GLatLng(43.187448,27.919918), e_europe[1] + "<br>" + e_europe[2], "overlay_number", offset),		// east-europe
		new ELabel(new GLatLng(49.644869,1.419918), europe[1] + "<br>" + europe[2], "overlay_number", offset),			// europe
		new ELabel(new GLatLng(24.415142,76.7207),  india[1] + "<br>" + india[2], "overlay_number", offset),			// india
		new ELabel(new GLatLng(1.810246,119.87695), indonesia[1] + "<br>" + indonesia[2], "overlay_number", offset),		// indonesia
		new ELabel(new GLatLng(28.659744,49.716793), middle_east[1] + "<br>" + middle_east[2], "overlay_number", offset),	// middle-east
		new ELabel(new GLatLng(65.3155,82.412106),  russia[1] + "<br>" + russia[2], "overlay_number", offset),			// russia
		new ELabel(new GLatLng(65.960532,20.712887), scandanavia[1] + "<br>" + scandanavia[2], "overlay_number", offset),	// scandanavia
		new ELabel(new GLatLng(39.524382,-98.100588), usa[1] + "<br>" + usa[2], "overlay_number", offset),			// usa

		new ELabel(new GLatLng(-58.052735,-156.474613), instructions, "instructions"),
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

		G_PHYSICAL_MAP.getMinimumResolution = function () { return 2 };
		G_NORMAL_MAP.getMinimumResolution = function () { return 2 };
		G_SATELLITE_MAP.getMinimumResolution = function () { return 2 };
		G_HYBRID_MAP.getMinimumResolution = function () { return 2 };

		figure_zoom();
		
		GEvent.addListener(map, "zoomend", figure_zoom);
		
		GEvent.addListener(map, "click", function(marker, point) {
			GDownloadUrl("/map_click/" + map.getZoom() + "_" + point.lat() + "_" + point.lng() + "/",
			
			function(data, responseCode) {
				json = eval(data);
				var mytabs = [
						new MaxContentTab('Based Here ' + json["base_t"],	json["base"]),
						new MaxContentTab('Flies Here ' + json["route_t"],	json["route"])
					];

				map.openMaxContentTabs(point, json["title"], json["title"], mytabs, {width: "300px"});
			});
		});
	}
}

function figure_zoom()
{	
	map.clearOverlays();
	
	if(map.getZoom() < 3 ){
		map.addOverlay(africa[0]);
		map.addOverlay(americas[0]);
		map.addOverlay(carribean[0]);
		map.addOverlay(alaska[0]);
		map.addOverlay(australia[0]);
		map.addOverlay(canada[0]);
		map.addOverlay(china[0]);
		map.addOverlay(e_europe[0]);
		map.addOverlay(europe[0]);
		map.addOverlay(india[0]);
		map.addOverlay(indonesia[0]);
		map.addOverlay(middle_east[0]);
		map.addOverlay(russia[0]);
		map.addOverlay(scandanavia[0]);
		map.addOverlay(usa[0]);
		
		for(i=0; i<labels.length; i++)
		{
			map.addOverlay(labels[i]);
		}
	}
	else
		map.addOverlay(BaseOverlay);
	
}

$(document).ready(function() {
		
	initialize();
	
});

window.onunload = GUnload;
