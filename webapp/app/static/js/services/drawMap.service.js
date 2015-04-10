angular.module('CampaignAdvisor')
  .factory('drawMap', ['stateFips', function (stateFips) {
  var drawMapService = {};
  var countyGeojson;
  var stateGeojson;
  var countiesByState;
  var svg;

	drawMapService.drawStates = function(id, data, toolTip){	
		var counties;
		var states;	
		var path = d3.geo.path();
		var california;
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
		function getStateId(stateName) {
			if (stateName) {
				return stateName.split(" ").join("");
			} else {
				return "undefined";
			}
		}
		function drawCounty(d) {
			var state = stateFips[d.properties.STATE];
			var stateFeatures = countiesByState[state];
			var stateId = getStateId(state);
			var countyOutlines = svg.append("g")
				.attr("id", stateId);
				countyOutlines.selectAll("path")
	      .data(stateFeatures.features)
		    .enter().append("path")
		    	.style('fill', 'black')
		    	.style("fill", 'white')
					.style("stroke", '#777')
		      .attr("d", path)
		      .on('click', function() {
		      	d3.selectAll('#' + stateId).remove();
		      });
			
			
		}


		$("#statesvg").remove();

		svg = d3.select("#stateContainer").append('svg')
					.attr('width', '600px')
					.attr('height', '900px')
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
      .on("click", drawCounty)
      .on("mouseover", function(d) {
      	d3.select('#' + getStateId(stateFips[d.properties.STATE] + '-state'))
      	.style('fill', '#ccc');
      })
      .on("mouseout", function(d) {
      	d3.select('#' + getStateId(stateFips[d.properties.STATE] + '-state'))
      	.style('fill', 'white');
      });
	};



	drawMapService.setGeojson = function(stateG, countyG) {
		stateGeojson = stateG;
		countyGeojson = countyG;
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

  return drawMapService;
  }]);
