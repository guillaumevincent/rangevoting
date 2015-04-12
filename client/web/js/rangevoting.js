'use strict';

var rangevotingModule = angular.module('rangevoting', ['ngRoute', 'restangular']);

rangevotingModule.config(['$routeProvider', '$locationProvider', function ($routeProvider) {
    $routeProvider.
        when('/', {
            templateUrl: 'static/pages/index.html',
            controller: 'createRangeVoteController'
        }).
        when('/rangevotes/:rangevoteId/admin/', {
            templateUrl: 'static/pages/admin.html',
            controller: 'adminRangeVoteController'
        }).
        otherwise({
            redirectTo: '/'
        });
}]);