angular.module('CampaignAdvisor')
  .controller('HomeController', ['$scope', 'countyLines', 'stateLines', 'drawMap', '$timeout', '$q', 'countyDataService',
  	function ($scope, countyLines, stateLines, drawMap, $timeout, $q, countyDataService) {
  	drawMap.setGeojson(stateLines, countyLines);
    drawMap.drawStates('#statesvg', {});

    var stateFips = ["10", "11", "12", "13", "15", "16", "17", "18", "19", "20", "21", "22", "23", "24", "25", "26", "27", "28", "29", "30", "31", "32", "33", "34", "35", "36", "37", "38", "39", "40", "41", "42", "44", "45", "46", "47", "48", "49", "50", "51", "53", "54", "55", "56", "01", "02", "04", "05", "06", "08", "09"];

    $scope.mapState = 'Show';
	 
    $scope.states        = loadAll();
    $scope.selectedItem  = null;
    $scope.searchText    = null;
    $scope.querySearch   = querySearch;
    function querySearch (query) {
      var results = query ? $scope.states.filter( createFilterFor(query) ) : [],
          deferred;
      if ($scope.simulateQuery) {
        deferred = $q.defer();
        $timeout(function () { deferred.resolve( results ); }, Math.random() * 1000, false);
        return deferred.promise;
      } else {
        return results;
      }
    }

    $scope.zoomToState = function(state) {
      drawMap.zoomToState(state.value);
    }

    $scope.mapZoomOut = function() {
      drawMap.reset();
    };
    /**
     * Build `states` list of key/value pairs
     */
    function loadAll() {
      var allStates = 'Alabama, Alaska, Arizona, Arkansas, California, Colorado, Connecticut, Delaware,\
              Florida, Georgia, Hawaii, Idaho, Illinois, Indiana, Iowa, Kansas, Kentucky, Louisiana,\
              Maine, Maryland, Massachusetts, Michigan, Minnesota, Mississippi, Missouri, Montana,\
              Nebraska, Nevada, New Hampshire, New Jersey, New Mexico, New York, North Carolina,\
              North Dakota, Ohio, Oklahoma, Oregon, Pennsylvania, Rhode Island, South Carolina,\
              South Dakota, Tennessee, Texas, Utah, Vermont, Virginia, Washington, West Virginia,\
              Wisconsin, Wyoming';
      return allStates.split(/, +/g).map( function (state) {
        return {
          value: state.toLowerCase(),
          display: state
        };
      });
    }
    /**
     * Create filter function for a query string
     */
    function createFilterFor(query) {
      var lowercaseQuery = angular.lowercase(query);
      return function filterFn(state) {
        return (state.value.indexOf(lowercaseQuery) === 0);
      };
    }
    $scope.drawAllCounties = function() {
      if ($scope.mapState == 'Show') {
        drawMap.drawAllCounties();
        $scope.mapState = 'Hide';
      } else {
        drawMap.removeAllCounties();
        $scope.mapState = 'Show';
      }
    }
    //$scope.drawAllCounties();

    $scope.loadDataPoints = function() {
    // Use timeout to simulate a 650ms request.
      $scope.dataPoints = []
      return $timeout(function() {
        countyDataService.getCountyStatisticsColumns().then(function(res) {
          $scope.dataPoints = res.data_points;
        });
      }, 1000);
    };

    $scope.$watch('dataPoint', function() {
      if ($scope.dataPoint) {
        countyDataService.getData($scope.dataPoint).then(function(countyData) {
          console.log(countyData);
          stateFips.forEach(function(fips) {
            drawMap.visualizeDataForState(fips, countyData);
          })
        });
      }
      
    });

    
    

    $scope.drawMap = drawMap;

  }]);
