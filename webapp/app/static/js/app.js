// Declare app level module which depends on filters, and services
angular.module('CampaignAdvisor', ['ngResource', 'ngRoute', 'ui.bootstrap', 'ui.date', 'ngMaterial', 'ngMdIcons'])
  .config(['$routeProvider', '$mdThemingProvider', function ($routeProvider, $mdThemingProvider) {
    $routeProvider
      .when('/map', {
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
    .when('/', {
      templateUrl: 'views/home/basicoverview.html', 
      controller: 'OverviewController'
    })
    .otherwise({redirectTo: '/'});

    $mdThemingProvider.theme('default')
      .primaryPalette('deep-purple')
      .accentPalette('pink');
  }]);
