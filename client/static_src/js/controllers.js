angular.module('rangevoting').controller('createRangeVoteController', ['$scope', function ($scope) {
    $scope.rangevote = {
        question: '',
        choices: []
    };

    $scope.isValid = true;

    $scope.rangevoteIsValid = function (form) {
        if(form){
            var choices = form.choices.split(',');
            return !!(form.question && choices.length > 1);
        }
        return false;
    };

    $scope.createRangevote = function (form) {

        if ($scope.rangevoteIsValid(form)) {
        }

    }
}]);