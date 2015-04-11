angular.module('rangevoting').controller('createRangeVoteController', ['$scope', function ($scope) {
    $scope.rangevote = {
        question : '',
        choices : []
    };
    $scope.createRangevote = function (rangevote) {
        console.log(rangevote);
    }
}]);