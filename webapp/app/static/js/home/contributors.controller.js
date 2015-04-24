angular.module('CampaignAdvisor')
  .controller('ContributorsController', ['$scope', '$timeout', function ($scope, $timeout) {
    $scope.header = 'Election Contributions';
    $scope.changeHeader = function(header) {
      $scope.header = header;
    };
    var tabTitles = ['Contribution by Occupation', 'Contribution by State', 'Do your contributions matter?']
    $scope.$watch('selectedIndex', function() {
      console.log($scope.selectedIndex);
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

  }]);
