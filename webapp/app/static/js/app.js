// Declare app level module which depends on filters, and services
angular.module('CampaignAdvisor', ['ngResource', 'ngRoute', 'ui.bootstrap', 'ui.date', 'ngMaterial'])
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/home/home.html', 
        controller: 'HomeController',
        resolve: {
      		countyLines: ['$http', function ($http){
      			return $http.get('/api/getCountyLines').then(
                    function success(response) { return response.data; },
                    function error(reason)     { return reason; }
                  );
      		}],
          stateLines: ['$http', function ($http){
            return $http.get('/api/getStateLines').then(
                    function success(response) { return response.data; },
                    function error(reason)     { return reason; }
                  );
          }]
    	  }
    })
    .when('/topcontributors', {
      templateUrl: 'views/home/topcontributors.html', 
      controller: 'ContributorsController'
    })
    .otherwise({redirectTo: '/'});
  }]);
