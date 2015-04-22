angular.module('CampaignAdvisor')
  .controller('ContributorsController', ['$scope', function ($scope) {
    var data = [['EXECUTIVE', 250.0], ['PRESIDENT', 150.0], ['PHYSICIAN', 100.0], ['LAWYER', 100.0], ['SELF-EMPLOYED', 100.0], ['NONE', 100.0], ['BUSINESS OWNER', 100.0], ['CEO', 100.0], ['REAL ESTATE', 100.0], ['CPA', 100.0], ['DENTIST', 100.0], ['FARMER', 100.0], ['BANKER', 100.0], ['FINANCE', 100.0], ['HOMEMAKER', 63.5], ['CONSULTANT', 56.0], ['ENGINEER', 55.0], ['SCIENTIST', 55.0], ['RETIRED', 50.0], ['PROFESSOR', 50.0], ['MANAGER', 50.0], ['SALES', 50.0], ['WRITER', 50.0], ['SOFTWARE ENGINEER', 50.0], ['ACCOUNTANT', 50.0], ['ARTIST', 50.0], ['PSYCHOLOGIST', 50.0], ['ADMINISTRATOR', 50.0], ['ARCHITECT', 50.0], ['REALTOR', 50.0], ['DIRECTOR', 50.0], ['MARKETING', 50.0], ['PHARMACIST', 50.0], ['ANALYST', 50.0], ['EXECUTIVE DIRECTOR', 50.0], ['DESIGNER', 50.0], ['SOFTWARE DEVELOPER', 50.0], ['OFFICE MANAGER', 40.0], ['EDITOR', 40.0], ['TEACHER', 35.0], ['NOT EMPLOYED', 35.0], ['EDUCATOR', 35.0], ['SOCIAL WORKER', 35.0], ['PROJECT MANAGER', 35.0], ['NURSE', 35.0], ['LIBRARIAN', 35.0], ['PSYCHOTHERAPIST', 35.0], ['MUSICIAN', 35.0], ['STUDENT', 31.5], ['DISABLED', 21.0]];
    
    var margin = {top: 40, right: 20, bottom: 30, left: 200},
        width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;


    var x = d3.scale.ordinal()
        .rangeRoundBands([0, width], .1);

    var y = d3.scale.linear()
        .range([height, 0]);

    var xAxis = d3.svg.axis()
        .scale(x)
        .orient("left");

    var yAxis = d3.svg.axis()
        .scale(y)
        .orient("bottom");
        

    var tip = d3.tip()
      .attr('class', 'd3-tip')
      .offset([-10, 0])
      .html(function(d) {
        return "<strong>Amount:</strong> <span style='color:red'>" + d[1] + "</span>";
      })

    var svg = d3.select("body").append("svg")
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
        .attr("transform", "translate(0," + height + ")")
        .call(xAxis);

    svg.append("g")
        .attr("class", "y axis")
        .call(yAxis)
      .append("text")
        .attr("y", 6)
        .attr("dy", ".71em")
        .style("text-anchor", "end")
        .text("Contribution Amt.");

    svg.selectAll(".bar")
        .data(data)
      .enter().append("rect")
        .attr("class", "bar")
        .attr("x", function(d) { return x(d[0]); })
        .attr("width", '15')
        .attr("y", function(d) { return y(d[1]); })
        .attr("height", function(d) { return height - y(d[1]); })
        .on('mouseover', tip.show)
        .on('mouseout', tip.hide)

  }]);
