angular.module('CampaignAdvisor')
  .controller('HomeController', ['$scope', 'countyLines', 'stateLines', 'drawMap', '$timeout', '$q', '$log',
  	function ($scope, countyLines, stateLines, drawMap, $timeout, $q, $log) {
  	drawMap.setGeojson(stateLines, countyLines);
	drawMap.drawStates('#statesvg', {});
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
      }
      
    }

    $scope.drawMap = drawMap;

  }]);
