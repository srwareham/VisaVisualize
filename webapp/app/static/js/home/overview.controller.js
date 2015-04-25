angular.module('CampaignAdvisor')
  .controller('OverviewController', ['$scope', '$location', function ($scope, $location) {
    $scope.headers = ['Analyzing voter interaction with presidential elections', 'Data sets and tools', 'Processing the data']
    $scope.header = $scope.headers[0];
    $scope.$watch('selectedIndex', function() {
      $scope.header = $scope.headers[$scope.selectedIndex]
    });
    $scope.nextPage = function(goTo) {
      $location.url(goTo);
    } 
  }]);
