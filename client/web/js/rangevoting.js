'use strict';

var rangevotingModule = angular.module('rangevoting', ['ngRoute', 'restangular']);

rangevotingModule.config(['$routeProvider', '$locationProvider', function ($routeProvider) {
    $routeProvider.
        when('/', {
            templateUrl: 'static/pages/index.html',
            controller: 'createRangeVoteController'
        }).
        when('/rangevotes/:id/admin/', {
            templateUrl: 'static/pages/admin.html',
            controller: 'adminRangeVoteController'
        }).
        when('/rangevotes/:id/', {
            templateUrl: 'static/pages/vote.html',
            controller: 'rangeVoteController'
        }).
        when('/rangevotes/:id/results/', {
            templateUrl: 'static/pages/results.html',
            controller: 'resultRangeVoteController'
        }).
        otherwise({
            redirectTo: '/'
        });
}]);