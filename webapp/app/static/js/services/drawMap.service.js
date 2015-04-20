angular.module('CampaignAdvisor')
  .factory('drawMap', ['stateFips', '$timeout', '$rootScope', function (stateFips, $timeout, $rootScope) {
  var drawMapService = {};
  var countyGeojson;
  var stateGeojson;
  var countiesByState;
  var stateGeojsonByState;
  var currentData;
  var stateCountyFips = {};
  var svg;
  var width = 600;
  var height = 900;
  var path = d3.geo.path();
  var counties;
	var states;	
	var zoomedIn = false;

	/**
	 * Colors
	 */
	// function createColorScale = function() {

	// };
	function createColorScale(min, max, minimumColor, maximumColor) {
		return d3.scale.linear().domain([min, max]).range([minimumColor, maximumColor]);
	}
	drawMapService.currentArea = 'United States of America';

	drawMapService.setCurrentArea = function(area) {
		drawMapService.currentArea = area;
	}

	drawMapService.getCurrentArea = function() {
		return drawMapService.currentArea;
	}
	function getStateId(stateName) {
		if (stateName) {
			return stateName.split(" ").join("");
		} else {
			return "undefined";
		}
	}
	var activeCountyDrawingId;
	function drawCounty(d) {
		if (!zoomedIn) return;
		if (activeCountyDrawingId) {
			d3.selectAll('#' + activeCountyDrawingId).remove();
		}
		var state = stateFips[d.properties.STATE];
		var stateFeatures = countiesByState[state];
		var stateId = getStateId(state);
		var boundsObj = getBoundsObj(d);
		var timeoutValue = 700;
		$timeout(function() {
			var countyOutlines = svg.append("g")
			.attr("id", stateId);
			countyOutlines.selectAll("path")
	  		.data(stateFeatures.features)
	    	.enter().append("path")
	    	.style('fill', 'black')
	    	.style("fill", 'white')
			.style("stroke", '#777')
			.attr("d", path)
			.attr('id', function(d) {
				var fipsCode = 'USA' + d.properties.STATE + d.properties.COUNTY;
				return fipsCode;
			})
			.style("stroke-width", 1.5 / boundsObj.scale + "px")
			.attr("transform", "translate(" + boundsObj.translate + ")scale(" + boundsObj.scale + ")")
			.on('click', function() {
				d3.selectAll('#' + stateId).remove();
			})
			.on('mouseover', function(d) {
				var countyName = d.properties.NAME;
				var label = state + ', ' + countyName;
				var dataForFips = getDataFromFips(d.properties.STATE + d.properties.COUNTY);
				label = dataForFips ? label + ' - ' + dataForFips : label;
				drawMapService.setCurrentArea(label);
				$rootScope.$apply();
			});
			if (currentData) {
				console.log(d.properties.STATE);
				drawMapService.visualizeDataForState(d.properties.STATE, currentData);
			}
		}, timeoutValue);

	  activeCountyDrawingId = stateId;
	}

	drawMapService.removeAllCounties = function() {
		stateGeojson.features.forEach(function(d) {
			var state = stateFips[d.properties.STATE];
			var stateId = getStateId(state);
			d3.selectAll('#' + stateId).remove();
		});
	}

	function drawCountySimple(d) {
		var state = stateFips[d.properties.STATE];
		var stateFeatures = countiesByState[state];
		var stateId = getStateId(state);
		var boundsObj = getBoundsObj(d);
		var timeoutValue = 700;
		var countyOutlines = svg.append("g")
		.attr("id", stateId);
		countyOutlines.selectAll("path")
  		.data(stateFeatures.features)
    	.enter().append("path")
    	.attr('id', function(d) {
			var fipsCode = 'USA' + d.properties.STATE + d.properties.COUNTY;
			return fipsCode;
		})
    	.style('fill', 'black')
    	.style("fill", 'white')
			.style("stroke", '#777')
      	.attr("d", path)
      	.on('mouseover', function(d) {
			var countyName = d.properties.NAME;
			var label = state + ', ' + countyName;
			var dataForFips = getDataFromFips(d.properties.STATE + d.properties.COUNTY);
			label = dataForFips ? label + ' - ' + dataForFips : label;
			drawMapService.setCurrentArea(label);
			$rootScope.$apply();
		});
	}

	function getDataFromFips(fips) {
		if (currentData && currentData[fips]) {
			return currentData[fips];
		}
		return '';
	}



	function colorCounty(d) {
		return "q" + Math.floor((Math.random() * 9)) + "-9";
	}

	drawMapService.drawAllCounties = function() {
		stateGeojson.features.forEach(function(d) {
			drawCountySimple(d);
		});
	};



	drawMapService.drawStates = function(id, data, toolTip){	
		function mouseOver(d){
			d3.select("#tooltip").transition().duration(200).style("opacity", .9);      
			var coordinates = d3.mouse(this);
			d3.select("#tooltip").html(toolTip(d.n, data[d.id]))  
			.style("left", coordinates[0] + "px")     
			.style("top", coordinates[1] + "px");
		}

		function mouseOut(){
			d3.select("#tooltip").transition().duration(500).style("opacity", 0);      
		}
		
		$("#statesvg").remove();

		svg = d3.select("#stateContainer").append('svg')
					.attr('width', width + 'px')
					.attr('height', height + 'px')
					.attr('id', 'statesvg'); 
		// create a container for states
		states = svg.append("g")
		    .attr("id", "states");
		// create a container for counties
		counties = svg.append("g")
		    .attr("id", "counties");
		states.selectAll("path")
		.data(stateGeojson.features)
		.enter().append("path")
		.style("fill", 'white')
		.style("stroke", '#777')
		.attr('id', function(d) { 
			return getStateId(stateFips[d.properties.STATE])  + '-state'; 
		})
		.attr("d", path)
		.on("click", drawMapService.zoomToState)
		.on("mouseover", function(d) {
			d3.select('#' + getStateId(stateFips[d.properties.STATE] + '-state'))
			.style('fill', '#ccc');
			drawMapService.setCurrentArea(d.properties.NAME);
			$rootScope.$apply();
		})
		.on("mouseout", function(d) {
			d3.select('#' + getStateId(stateFips[d.properties.STATE] + '-state'))
			.style('fill', 'white');
		});

	};

	var selectedArea = d3.select(null);

	function getBoundsObj(d) {
		var bounds = path.bounds(d),
	      dx = bounds[1][0] - bounds[0][0],
	      dy = bounds[1][1] - bounds[0][1],
	      x = (bounds[0][0] + bounds[1][0]) / 2,
	      y = (bounds[0][1] + bounds[1][1]) / 2,
	      scale = .6 / Math.max(dx / width, dy / height),
	      translate = [width / 2 - scale * x, height / 2 - scale * y];
	  return {
	  	scale: scale,
	  	translate: translate
	  };
	}
	/**
	 * Reference from mbostock
	 * @param  {[type]} d [description]
	 * @return {[type]}   [description]
	 */
	function zoomToGeojson(d, physicalCall) {
	  var boundsObj = getBoundsObj(d);
	  states.transition()
	      .duration(750)
	      .style("stroke-width", 1.5 / boundsObj.scale + "px")
	      .attr("transform", "translate(" + boundsObj.translate + ")scale(" + boundsObj.scale + ")");
	}

	drawMapService.reset = function() {
		zoomedIn = false;
		if (activeCountyDrawingId) {
			d3.selectAll('#' + activeCountyDrawingId).remove();
		}
	  selectedArea.classed("active", false);
	  selectedArea = d3.select(null);

	  states.transition()
      .duration(750)
      .style("stroke-width", "1px")
      .attr("transform", "");
	}

	drawMapService.setGeojson = function(stateG, countyG) {
		stateGeojson = stateG;
		countyGeojson = countyG;
		stateGeojsonByState = stateGeojson.features.reduce(function(data, feature) {
			data[feature.properties.NAME.toLowerCase()] = feature;
			return data;
		}, {});
		countiesByState = countyGeojson.features.map(function(feature) {
			var stateFips = feature.properties.STATE; 
			if (!stateCountyFips[stateFips]) {
				stateCountyFips[stateFips] = [];
			}
			stateCountyFips[stateFips].push(stateFips + feature.properties.COUNTY);
			return {
				state: feature.properties.STATE,
				feature: feature
			};
		}).reduce(function(data, feature) {
			if (feature.state && parseInt(feature.state)) {
				var key = stateFips[feature.state];
				if (!data[key]) {
					data[key] = {
						"type": "FeatureCollection",
						"features": []
					};
				}
				data[key].features.push(feature.feature);
			}
			return data;
		}, {});
	};


	drawMapService.zoomToState = function(state) {
		zoomedIn= true;
		selectedArea.classed("active", false);
		var geojson;
		if (!state.properties) {
			geojson = stateGeojsonByState[state];
		} else {
			geojson = state;
		}
		var id = getStateId(stateFips[geojson.properties.STATE])  + '-state';
		selectedArea = d3.select('#' + id);
		zoomToGeojson(geojson);
		drawCounty(geojson);
	};

	drawMapService.visualizeDataForState = function(stateFips, countyData) {
		var countyFips = stateCountyFips[stateFips];
		var min = countyData.min;
		var max = countyData.max;
		var colorScale = createColorScale(countyData.min, countyData.max, d3.rgb('white'), d3.rgb('blue').brighter(100));
		countyData = countyData.countyData;
		currentData = countyData;
		if (!countyFips) return;
		countyFips.forEach(function(fips) {
			d3.select('#USA' + fips)
				.style('fill', function() {
					if (countyData && countyData[fips]) {
						return colorScale(countyData[fips]);
					} else {	
						return 'black';
					}
				});
		});
	};

  return drawMapService;
  }]);
