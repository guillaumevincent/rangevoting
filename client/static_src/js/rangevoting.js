'use strict';

var rangevotingModule = angular.module('rangevoting', ['ngRoute', 'restangular']);

rangevotingModule.config(['$routeProvider', '$locationProvider', function ($routeProvider, $locationProvider) {
    $routeProvider.
        when('/', {
            templateUrl: 'static/pages/index.html',
            controller: 'createRangeVoteController'
        }).
        otherwise({
            redirectTo: '/'
        });
    $locationProvider.html5Mode(true);
}]);