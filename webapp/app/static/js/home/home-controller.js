angular.module('CampaignAdvisor')
  .controller('HomeController', ['$scope', 'countyLines', 'stateLines', 'drawMap', '$timeout', '$q', '$log',
  	function ($scope, countyLines, stateLines, drawMap, $timeout, $q, $log) {
  	drawMap.setGeojson(stateLines, countyLines);
	drawMap.drawStates('#statesvg', {});

	// , function (n, d){	/* function to create html content string in tooltip div. */
	// 	return "<div style='background:white;border-radius:0px;width:300px;height:200px; padding:0px;border-radius:0px;'>" +
	// 	"<h3 style='font-family:circular;color:black;padding:20px;width:100%'>"+n+"</h3><table>"+
	// 	"</table></div>";
	// }

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
  }]);
