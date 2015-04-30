angular.module('CampaignAdvisor')
  .controller('ContributorsController', ['$scope', '$timeout', '$location', function ($scope, $timeout, $location) {
    $scope.header = 'Election Contributions';
    $scope.changeHeader = function(header) {
      $scope.header = header;
    };
    $scope.nextPage = function(goTo) {
      $location.url(goTo);
    };

    $scope.rankStatesPerCap = ['district of columbia', 'illinois', 'massachusetts', 'connecticut', 'vermont', 'maryland', 'wyoming', 'colorado', 'virginia', 'utah'];
    var tabTitles = ['Contribution by Occupation', 'Contribution by County', 'Contribution by State', 'Contribution by County Size']
    $scope.$watch('selectedIndex', function() {
      if ($scope.selectedIndex != -1) {
        $scope.changeHeader(tabTitles[$scope.selectedIndex]);
      }
    });
    /* Draw first visualization */
    $timeout(function() {

      var data = [['EXECUTIVE', 250.0], ['PRESIDENT', 150.0], ['PHYSICIAN', 100.0], ['LAWYER', 100.0], ['SELF-EMPLOYED', 100.0], ['NONE', 100.0], ['BUSINESS OWNER', 100.0], ['CEO', 100.0], ['REAL ESTATE', 100.0], ['CPA', 100.0], ['DENTIST', 100.0], ['FARMER', 100.0], ['BANKER', 100.0], ['FINANCE', 100.0], ['HOMEMAKER', 63.5], ['CONSULTANT', 56.0], ['ENGINEER', 55.0], ['SCIENTIST', 55.0], ['RETIRED', 50.0], ['PROFESSOR', 50.0], ['MANAGER', 50.0], ['SALES', 50.0], ['WRITER', 50.0], ['SOFTWARE ENGINEER', 50.0], ['ACCOUNTANT', 50.0], ['ARTIST', 50.0], ['PSYCHOLOGIST', 50.0], ['ADMINISTRATOR', 50.0], ['ARCHITECT', 50.0], ['REALTOR', 50.0], ['DIRECTOR', 50.0], ['MARKETING', 50.0], ['PHARMACIST', 50.0], ['ANALYST', 50.0], ['EXECUTIVE DIRECTOR', 50.0], ['DESIGNER', 50.0], ['SOFTWARE DEVELOPER', 50.0], ['OFFICE MANAGER', 40.0], ['EDITOR', 40.0], ['TEACHER', 35.0], ['NOT EMPLOYED', 35.0], ['EDUCATOR', 35.0], ['SOCIAL WORKER', 35.0], ['PROJECT MANAGER', 35.0], ['NURSE', 35.0], ['LIBRARIAN', 35.0], ['PSYCHOTHERAPIST', 35.0], ['MUSICIAN', 35.0], ['STUDENT', 31.5], ['DISABLED', 21.0]];
      data = data.map(function(dataPoint) {
        dataPoint[0] = dataPoint[0].substring(0,1) + dataPoint[0].substring(1).toLowerCase();
        return dataPoint;
      });
      var margin = {top: 40, right: 20, bottom: 30, left: 200},
          width = 960 - margin.left - margin.right,
          height = 500 - margin.top - margin.bottom;


      var x = d3.scale.ordinal()
          .rangeRoundBands([0, width], .1);

      var y = d3.scale.linear()
          .range([0, width]);

      var xAxis = d3.svg.axis()
          .scale(x)
          .orient("left");

      var yAxis = d3.svg.axis()
          .scale(y)
          .orient("top");
          

      var tip = d3.tip()
        .attr('class', 'd3-tip')
        .style('font-size', '12px')
        .style('font-family', 'RobotoDraft')
        .offset([-10, 0])
        .html(function(d) {
          return  "<div><span style='text-transform: uppercase'>Occupation:</span> <span style='color:#FF4081;font-weight:bold;font-size:20px !important;'>" + d[0] + "</span></div>" + 
           "<div style='text-transform: uppercase;'>Amount:<span style='color:#FF4081;font-weight:bold;font-size:20px !important;'>" + d[1] + "</span></div>";
        })

      var svg = d3.select("#topcontributors").append("svg")
          .attr("width", width + margin.left + margin.right)
          .attr("height", height + margin.top + margin.bottom)
        .append("g")
          .attr("transform", "translate(" + margin.left + "," + margin.top + ")");
      svg.call(tip);

      x.domain(data.map(function(d) { return d[0]; }));
      var maxValue = d3.max(data, function(d) { return d[1]; });
      y.domain([0, maxValue + 50]);

      svg.append("g")
          .attr("class", "x axis")
          .call(xAxis);

      svg.append("g")
          .attr("class", "y axis")
          .call(yAxis)
        .append("text")
          .attr("y", -15)
          .attr('x', width + 140)
          .attr("dy", ".71em")
          .style("text-anchor", "end")
          .style('font-family', 'RobotoDraft')
          .style('font-size', '15px')
          .text("Contribution Amt.");
      function indexOfData(jobTitle) {
        for (var i = 0; i < data.length; i++) {
          var dataPoint = data[i][0];
          if (dataPoint == jobTitle) {
            return i;
          }
        }
        return -1;
      }
      svg.selectAll(".bar")
          .data(data)
        .enter().append("rect")
          .attr("class", "bar")
          .attr("x", function(d) { return 0; })
          .attr("height", '10')
          .attr("y", function(d) { 
            var index = indexOfData(d[0]);
            return index * 10 + index * 4 + 22.5;
          })
          .attr("width", function(d) { return y(d[1]); })
          .on('mouseover', tip.show)
          .on('mouseout', tip.hide)


  }, 1000);
  /**
   * County contributions
   */
  $scope.countyContributions = {
    democrats: {
      count: [['california', 'los angeles'],['illinois', 'cook'], ['new york', 'new york'],['washington', 'king'],['district of columbia', 'district of columbia'],['massachusetts', 'middlesex'],['california', 'alameda'], ['maryland', 'montgomery'], ['california', 'san diego'], ['california', 'san francisco'],['california', 'santa clara'],['texas', 'harris'], ['new york', 'kings'], ['arizona', 'maricopa'], ['virginia', 'fairfax'], ['california', 'orange'], ['texas', 'travis'], ['minnesota', 'hennepin'], ['new york', 'westchester'], ['texas', 'dallas']],
      sum: 0
    },
    republicans: {
      count: [['california', 'los angeles'],['texas', 'harris'], ['arizona', 'maricopa'], ['california', 'orange'], ['california', 'san diego'], ['virginia', 'fairfax'], ['new york', 'new york'], ['illinois', 'cook'], ['connecticut', 'fairfield'], ['texas', 'dallas'], ['utah', 'salt lake'],['georgia', 'fulton'], ['florida', 'palm beach'], ['utah', 'utah'],['washington', 'king'], ['michigan', 'oakland'],['massachusetts', 'middlesex'], ['nevada', 'clark'], ['florida', 'miami-dade'], ['maryland', 'montgomery']],
      sum: 0
    }
  };

  $scope.formatStateName = function(description, index) {
    var original = description.split(' ');
    return (index + 1)  + '. ' + original.map(function(v) {
      if (v == 'of') return v;
      return v.substring(0,1).toUpperCase() + v.substring(1);
    }).join(' ');
  };

  /**
   * State contributions
   */
  $timeout(function() {

    function getTooltip(d){ /* function to create html content string in tooltip div. */
      var states = d.data.states;
      height = states.length * 28 + 40;
      height = height < 400 ? 400 : height;
      var tooltipData = "<div style='background:rgba(0,0,0,0.2);border-radius:0px;width:300px;height:" + height + "px;padding:0px;border-radius:0px;'><div style='padding:20px;'>" + 
      "<h3 style='font-family:RobotoDraft; color:rgb(255,64,129);font-size:30px;padding:5px;width:100%'>"+ (d.data.percent * 100).toFixed(2) + '%' +"</h3>"; 
      
      for (var i = 0; i < states.length; i++) {
        var name = states[i].substring(0, 1).toUpperCase() + states[i].substring(1);
        tooltipData = tooltipData + "<div style='font-family:RobotoDraft;color:black;font-size:20px;'>" + name + "</div>"; 
      }
      // "<div style='font-family:Lato;color:black;font-size:20px;'>R-squared - " + "<span style='font-family:circular;color:black;font-size:20px;'>" + (d.r_squared) + "</span></div>" + 
      // "<div style='font-family:Lato;color:black;font-size:20px;'>Performance - " + "<span style='font-family:circular;color:black;font-size:20px;'>" + (d.performance) + "</span></div>" + 
      // "</table></div>";
      
      return tooltipData + "</div></div>";
    }
    var width = 960,
    height = 500,
    radius = Math.min(width, height) / 2;

    var arc = d3.svg.arc()
        .outerRadius(radius - 10)
        .innerRadius(0);

    var pie = d3.layout.pie()
        .sort(null)
        .value(function(d) {
          return  d.percent * 100; 
        });
    var colors = [['#F44336','#FFCDD2'], ['#00BCD4','#B2EBF2'], ['#009688', '#B2DFDB'],['#FFEB3B','#FFF9C4']];
    var svg = d3.select("#statecontributions").append("svg")
        .attr("width", width)
        .attr("height", height)
        .style('padding-bottom', '100px')
      .append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");
    var stateContributions = [{'states': ['california', 'illinois', 'texas', 'new york', 'florida', 'massachusetts'], 'percent': 0.51028471133206421}, {'states': ['virginia', 'pennsylvania', 'maryland', 'new jersey', 'washington', 'georgia', 'ohio', 'colorado', 'michigan', 'north carolina'], 'percent': 0.24867052205744031}, {'states': ['connecticut', 'district of columbia', 'arizona', 'tennessee', 'minnesota', 'missouri', 'utah', 'oregon', 'wisconsin', 'louisiana'], 'percent': 0.13221005285822571}, {'states': ['indiana', 'oklahoma', 'nevada', 'south carolina', 'alabama', 'kentucky', 'new mexico', 'iowa', 'kansas', 'new hampshire', 'mississippi', 'idaho', 'arkansas', 'maine', 'nebraska', 'hawaii', 'vermont', 'montana', 'wyoming', 'alaska', 'rhode island', 'west virginia', 'delaware', 'south dakota', 'north dakota'], 'percent': 0.10883471375226984}];
    var g = svg.selectAll(".arc")
      .data(pie(stateContributions))
      .enter().append("g")
        .attr("class", "arc");
    g.append("path")
      .attr("d", arc)
      .attr('id', function(d, i) {
        return 'states-' + i;
      })
      .style("fill", function(d,i) { 
        return colors[i][0];
      })
      .on('mouseover', function(d,i) {
        d3.select('#states-' + i).style('fill', colors[i][1]);
        d3.select("#tooltip").transition().duration(200).style("opacity", .9);      
        var coordinates = d3.mouse(this);
        d3.select("#tooltip").html(getTooltip(d))
        .style("left", coordinates[0] + (width / 2) + "px")     
        .style("top", coordinates[1] + (height / 2) + "px");
      })
      .on('mouseout', function(d,i) {
        d3.select('#states-' + i).style('fill', colors[i][0]);
        d3.select("#tooltip").transition().duration(500).style("opacity", 0); 
      });
    g.append("text")
      .attr("transform", function(d) { 
        var t = arc.centroid(d);
        return "translate(" + t[0]*1.2 +"," + t[1]*1.2 + ")";
      })
      .attr("dy", ".35em")
      .style("text-anchor", "middle")
      .style('font-family', 'RobotoDraft')
      .style('font-size', '20px')
      .style('weight', 'normal')
      .text(function(d) { 
        return d.data.states.length + ' states';
      })
      .on('mouseover', function(d,i) {
        d3.select('#states-' + i).style('fill', colors[i][1]);
      })
      .on('mouseout', function(d,i) {
        d3.select('#states-' + i).style('fill', colors[i][0]);
      });
  }, 1000);
/**
   * State contributions
   */
  $timeout(function() {
    var width = 960,
    height = 600,
    radius = Math.min(width, height) / 2;

    var arc = d3.svg.arc()
        .outerRadius(radius - 10)
        .innerRadius(0);

    var pie = d3.layout.pie()
        .sort(null)
        .value(function(d) {
          return  d.value; 
        });
    var colors = ['#3366CC', '#DC3912', '#FF9900', '#109618', '#990099'];
    var svg = d3.select("#county-contributions-size").append("svg")
        .attr("width", width)
        .attr("height", height)
        .style('padding-top','80px')
        .style('padding-bottom', '80px')
      .append("g")
        .attr("transform", "translate(" + width / 2 + "," + height / 2 + ")");
    var countyContributions = [{
      type: 'Huge',
      count: 80,
      value: 51.2,
      distance: 2.5,
      index: 0
    }, {
      type: 'Large',
      count: 406,
      value: 37.4,
      distance: 2.6,
      index: 1
    }, {
      type: 'Medium',
      count: 470,
      value: 6.1,
      distance: 2.3,
      index: 2
    }, {
      type: 'Small',
      count: 1856,
      value: 5.2,
      distance: 2.3,
      index: 3
    }, {
      type: 'Tiny',
      count: 310,
      value: 0.1,
      distance: 2.1,
      index: 4
    }];
    var g = svg.selectAll(".arc")
      .data(pie(countyContributions))
      .enter().append("g")
        .attr("class", "arc");
    g.append("path")
      .attr("d", arc)
      .attr('id', function(d, i) {
        return 'states-' + i;
      })
      .style("fill", function(d,i) { 
        return colors[i];
      })
      .on('mouseover', function(d, i) {
        angular.element('#' + d.data.type + 'County').css('background-color', '#ccc');
      })
      .on('mouseout', function(d) {
        angular.element('#' + d.data.type + 'County').css('background-color', 'white');
      })
    g.append("text")
      .attr("transform", function(d) { 
        var t = arc.centroid(d);
        if (d.data.type == 'Huge') {
          return "translate(" + t[0]*(d.data.distance - 1) +"," + t[1]*(d.data.distance + 50) + ")";
        }
        return "translate(" + t[0]*d.data.distance +"," + t[1]*d.data.distance + ")";
      })
      .on('mouseover', function(d, i) {
        $scope.currentCountyData = d.data;
      })
      .attr("dy", ".35em")
      .style("text-anchor", "middle")
      .style('font-family', 'RobotoDraft')
      .style('font-size', '15px')
      .style('weight', 'normal')
      .text(function(d) { 
        return d.data.count + ' ' + d.data.type + ' counties';
      })
      .on('mouseover', function(d, i) {
        angular.element('#' + d.data.type + 'County').css('background-color', '#ccc');
      })
      .on('mouseout', function(d) {
        angular.element('#' + d.data.type + 'County').css('background-color', 'white');
      })
  }, 1000);

  $scope.sizeData = [{
    type: 'Huge',
    text: '691487+'
  }, {
    type: 'Large',
    text: '10000 - 691487'
  }, {
    type: 'Medium',
    text: '50000 - 100000'
  }, {
    type: 'Small',
    text: '4078 - 50000'
  }, {
    type: 'Tiny',
    text: '1 - 4078'
  }];

  }]);
