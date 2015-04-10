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


	//drawMap.drawCounties('#statesvg', countyLines);
	//
	//var self = this;
    // list of `state` value/display objects
    $scope.states        = loadAll();
    $scope.selectedItem  = null;
    $scope.searchText    = null;
    $scope.querySearch   = querySearch;
    $scope.simulateQuery = false;
    $scope.isDisabled    = false;
    $scope.selectedItemChange = selectedItemChange;
    $scope.searchTextChange   = searchTextChange;
    // ******************************
    // Internal methods
    // ******************************
    /**
     * Search for states... use $timeout to simulate
     * remote dataservice call.
     */
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
    function searchTextChange(text) {
      $log.info('Text changed to ' + text);
    }
    function selectedItemChange(item) {
      $log.info('Item changed to ' + item);
    }
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
