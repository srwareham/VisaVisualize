angular.module('CampaignAdvisor')
  .factory('countyDataService', ['$resource', function ($resource) {
  	var countyDataService = {};
  	var countyStatisticsResource = $resource('/api/getCountyStatistics', {}, {
      getCountyStatistics: {
        method: 'POST'
      }, 
      getCountyStatisticsColumns: {
      	method: 'GET',
      	url: '/api/getCountyStatisticsColumns'
      }
    });
    var PERCENTAGE_DATA = ['percent', 'Pct', 'pct', 'percentage', 'Change'];
  	countyDataService.getData = function(columnName) {
  		return countyStatisticsResource.getCountyStatistics({ data_column: columnName}).$promise.then(function (countyData) {
  			return countyDataService.normalizeData(columnName, countyData);
  		});
  	};
  	countyDataService.normalizeData = function(columnName, countyData) {
  		var min = countyData.min_value;
  		var max = countyData.max_value;
  		countyData = countyData.county_data;
  		var isPct = PERCENTAGE_DATA.some(function(str) {
        return columnName.indexOf(str) != -1;
      });
  		var dataArray = Object.keys(countyData).map(function(countyDataKey) {
  			var dataPoint = [];
  			dataPoint[0] = countyDataKey;
  			dataPoint[1] = countyData[countyDataKey];
  			return dataPoint;
  		});
  		if (isPct) {
        var data;
        if (columnName === 'percent_vote_gop' || columnName === 'percent_vote_democrat') {
          data = transformToObj(dataArray, true);
          min = min * 100;
          max = max * 100;
        } else {
          data = transformToObj(dataArray);
        }
  			return { countyData: data, min: min, max: max} ;
  		} else {
  			var range = max - min;
        dataArray = dataArray.sort(function(a, b) {
          return b[1] - a[1];
        });
        dataArray = dataArray.slice(10);
        var max = -1;
        var min = 101;
  			dataArray = dataArray.map(function(d) {
  				d[1] = (d[1] - min) / range * 100;
          if (d[1] > max) {
            max = d[1];
          }
          if (d[1] < min){
            min = d[1];
          }
  				return d;
  			});
  			return { countyData: transformToObj(dataArray), min: min, max: max} ;
  		}
  	};

  	countyDataService.getCountyStatisticsColumns = function() {
  		return countyStatisticsResource.getCountyStatisticsColumns().$promise;
  	}

  	function transformToObj(normalizedData, multiply) {
  		return normalizedData.reduce(function(accum, data) {
  			accum[data[0]] = multiply ? data[1] * 100 : data[1];
  			return accum;
  		}, {});
  	}
    return countyDataService;
  }]);
