// Declare app level module which depends on filters, and services
angular.module('CampaignAdvisor', ['ngResource', 'ngRoute', 'ui.bootstrap', 'ui.date'])
  .config(['$routeProvider', function ($routeProvider) {
    $routeProvider
      .when('/', {
        templateUrl: 'views/home/home.html', 
        controller: 'HomeController',
        resolve: {
    		countyLines: ['$http', function ($http){
    			return $http.get('/api/getCountyLines').then(
                  function success(response) { return response; },
                  function error(reason)     { return reason; }
                );
    		}]
    	}
    })
    .otherwise({redirectTo: '/'});
  }]);
