angular.module('CampaignAdvisor')
  .factory('drawMap', ['stateFips', '$timeout', function (stateFips, $timeout) {
  var drawMapService = {};
  var countyGeojson;
  var stateGeojson;
  var countiesByState;
  var stateGeojsonByState;
  var svg;
  var width = 600;
  var height = 900;
  var path = d3.geo.path();
  var counties;
	var states;	
	var zoomedIn = false;
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
	      .style("stroke-width", 1.5 / boundsObj.scale + "px")
	      .attr("transform", "translate(" + boundsObj.translate + ")scale(" + boundsObj.scale + ")")
	      .on('click', function() {
	      	d3.selectAll('#' + stateId).remove();
	      });
		}, timeoutValue);
	  console.log('asdas');
	  activeCountyDrawingId = stateId;
	}
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

  return drawMapService;
  }]);
