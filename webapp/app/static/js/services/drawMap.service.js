angular.module('CampaignAdvisor')
  .factory('drawMap', ['stateFips', '$timeout', '$rootScope', function (stateFips, $timeout, $rootScope) {
  var drawMapService = {};
  var countyGeojson;
  var stateGeojson;
  var countiesByState;
  var stateGeojsonByState;
  var currentData = {};
  var stateCountyFips = {};
  var svgMap = {};
  var width = 533.33;
  var height = 800;
  var projection = d3.geo.albersUsa()
    .scale(width)
    .translate([width / 2, height / 2]);
  var path = d3.geo.path(projection);
  var counties = {};
	var states = {};
	var zoomedIn = {
		1: false,
		2: false
	};
	var BASIC_DESCRIPTION = 'United States of America';

	/**
	 * Colors
	 */
	// function createColorScale = function() {

	// };
	function createColorScale(min, max, minimumColor, maximumColor) {
		return d3.scale.linear().domain([min, 0,  max]).range([minimumColor, d3.rgb('white'), maximumColor]);
	}
	drawMapService.currentArea =  {}

	drawMapService.setCurrentArea = function(area, mapNumber) {
		drawMapService.currentArea[mapNumber] = area;
	}

	drawMapService.getCurrentArea = function(mapNumber) {
		return drawMapService.currentArea[mapNumber];
	}
	function getStateId(stateName) {
		if (stateName) {
			return stateName.split(" ").join("");
		} else {
			return "undefined";
		}
	}
	var activeCountyDrawingId = {};
	function drawCounty(d, mapNumber) {
		if (!zoomedIn[mapNumber]) return;
		if (activeCountyDrawingId[mapNumber]) {
			d3.selectAll('#' + activeCountyDrawingId[mapNumber]).remove();
		}
		var state = stateFips[d.properties.STATE];
		var stateFeatures = countiesByState[state];
		var stateId = getStateId(state);
		var boundsObj = getBoundsObj(d);
		var timeoutValue = 700;
		var svg = svgMap[mapNumber];
		$timeout(function() {
			var countyOutlines = svg.append("g")
			.attr("id", stateId + mapNumber);
			countyOutlines.selectAll("path")
	  		.data(stateFeatures.features)
	    	.enter().append("path")
	    	.style('fill', 'black')
	    	.style("fill", 'white')
			.style("stroke", '#777')
			.attr("d", path)
			.attr('id', function(d) {
				var fipsCode = 'USA' + mapNumber + d.properties.STATE + d.properties.COUNTY;
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
				label = dataForFips ? label + ': ' + dataForFips : label;

				drawMapService.setCurrentArea(label, mapNumber);
				var fipsCode = 'USA' + d.properties.STATE + d.properties.COUNTY;
				//d3.select('#' + fipsCode).
				//style('fill', '#ccc');
				$rootScope.$apply();
			})
			.on('mouseout', function(d) {
				var fipsCode = 'USA' + d.properties.STATE + d.properties.COUNTY;
				// d3.select('#' + fipsCode).
				// style('fill', '#fff');
			});
			if (currentData[mapNumber]) {
				drawMapService.visualizeDataForState(d.properties.STATE, mapNumber);
			}
		}, timeoutValue);

	  activeCountyDrawingId[mapNumber] = stateId + mapNumber;
	}

	drawMapService.setCurrentData = function(_data, mapNumber) {
		currentData[mapNumber] = _data;
	}

	drawMapService.removeAllCounties = function(mapNumber) {
		stateGeojson.features.forEach(function(d) {
			var state = stateFips[d.properties.STATE];
			var stateId = getStateId(state);
			d3.selectAll('#' + stateId + mapNumber).remove();
		});
	}

	function drawCountySimple(d, mapNumber) {
		var state = stateFips[d.properties.STATE];
		var stateFeatures = countiesByState[state];
		var stateId = getStateId(state);
		var boundsObj = getBoundsObj(d);
		var timeoutValue = 700;
		var svg = svgMap[mapNumber];
		var countyOutlines = svg.append("g")
		.attr("id", stateId + mapNumber);
		countyOutlines.selectAll("path")
  		.data(stateFeatures.features)
    	.enter().append("path")
    	.attr('id', function(d) {
			var fipsCode = 'USA' + mapNumber + d.properties.STATE + d.properties.COUNTY;
			return fipsCode;
		})
    	.style('fill', 'black')
    	.style("fill", 'white')
			.style("stroke", '#777')
      	.attr("d", path)
      	.on('mouseover', function(d) {
			var countyName = d.properties.NAME;
			var label = state + ', ' + countyName;
			var dataForFips = getDataFromFips(d.properties.STATE + d.properties.COUNTY, mapNumber);
			label = dataForFips ? label + ': ' + dataForFips : label;
			drawMapService.setCurrentArea(label, mapNumber);
			$rootScope.$apply();
		});
	}

	function getDataFromFips(fips, mapNumber) {
		if (!currentData[mapNumber]) return '';
		if (currentData[mapNumber].countyData && currentData[mapNumber].countyData[fips]) {
			return currentData[mapNumber].countyData[fips].toFixed(2);
		}
		return '';
	}



	function colorCounty(d) {
		return "q" + Math.floor((Math.random() * 9)) + "-9";
	}

	drawMapService.drawAllCounties = function(mapNumber) {
		stateGeojson.features.forEach(function(d) {
			drawCountySimple(d, mapNumber);
		});
		// if (currentData[mapNumber]) {
		// 	var stateFips = ["10", "11", "12", "13", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "44", "45", "46", "47", "48", "49", "50", "51", "53", "54", "55", "56", "01", "02", "04", "05", "06", "08", "09"];

		// }
	};



	drawMapService.drawStates = function(mapNumber){	
		
		svgMap[mapNumber] = d3.select("#stateContainer" + mapNumber).append('svg')
					.attr('width', width + 'px')
					.attr('height', height + 'px')
					.attr('id', 'statesvg' + mapNumber); 
		var svg = svgMap[mapNumber];

		drawMapService.currentArea[mapNumber] = BASIC_DESCRIPTION;
		// create a container for states
		states[mapNumber] = svg.append("g")
		    .attr("id", "states")
		    .attr('width', width)
			.attr('height', height)
		// create a container for counties
		counties[mapNumber] = svg.append("g")
		    .attr("id", "counties");
		states[mapNumber].selectAll("path")
		.data(stateGeojson.features)
		.enter().append("path")
		.style("fill", 'white')
		.style("stroke", '#777')
		.attr('id', function(d) { 
			return getStateId(stateFips[d.properties.STATE])  + '-state' + mapNumber; 
		})
		.attr("width", width)
        .attr("height", height)
		.attr("d", path)
		.on("click", drawMapService.zoomToState(mapNumber))
		.on("mouseover", function(d) {
			d3.select('#' + getStateId(stateFips[d.properties.STATE] + '-state') + mapNumber)
			.style('fill', '#ccc');
			drawMapService.setCurrentArea(d.properties.NAME, mapNumber);
			$rootScope.$apply();
		})
		.on("mouseout", function(d) {
			d3.select('#' + getStateId(stateFips[d.properties.STATE] + '-state') + mapNumber)
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
	function zoomToGeojson(d, mapNumber) {
	  var boundsObj = getBoundsObj(d);
	  states[mapNumber].transition()
	      .duration(750)
	      .style("stroke-width", 1.5 / boundsObj.scale + "px")
	      .attr("transform", "translate(" + boundsObj.translate + ")scale(" + boundsObj.scale + ")");
	}

	drawMapService.reset = function(mapNumber) {
		zoomedIn[mapNumber] = false;
		if (activeCountyDrawingId[mapNumber]) {
			d3.selectAll('#' + activeCountyDrawingId[mapNumber]).remove();
		}
	  selectedArea.classed("active", false);
	  selectedArea = d3.select(null);

	  states[mapNumber].transition()
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


	drawMapService.zoomToState = function(mapNumber) {
		return function(state) {
			zoomedIn[mapNumber]= true;
			selectedArea.classed("active", false);
			var geojson;
			if (!state.properties) {
				geojson = stateGeojsonByState[state];
			} else {
				geojson = state;
			}
			var id = getStateId(stateFips[geojson.properties.STATE])  + '-state' + mapNumber;
			selectedArea = d3.select('#' + id);
			zoomToGeojson(geojson, mapNumber);
			drawCounty(geojson, mapNumber);
		}
		
	};

	drawMapService.visualizeDataForState = function(stateFips, mapNumber) {
		if (!currentData[mapNumber]) {
			return;
		}
		countyData = currentData[mapNumber];
		var countyFips = stateCountyFips[stateFips];
		var min = countyData.min;
		var max = countyData.max;
		var colorScale = createColorScale(countyData.min, countyData.max, d3.rgb('red').brighter(100), d3.rgb('blue').brighter(100));
		
		countyData = countyData.countyData;
		if (!countyFips) return;
		countyFips.forEach(function(fips) {
			d3.select('#USA' + mapNumber + fips)
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
