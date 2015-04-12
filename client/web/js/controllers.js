angular.module('rangevoting').controller('createRangeVoteController', ['$scope', '$location', 'Restangular', function ($scope, $location, Restangular) {
    $scope.isValid = true;

    $scope.rangevoteIsValid = function (rangevote) {
        return !!(rangevote.question && rangevote.choices.length > 1);
    };

    $scope.convertRangeVote = function (form) {
        var rangevote = {question: '', choices: []};
        if (form) {
            rangevote.question = form.question;
            rangevote.choices = _.map(form.choices.split(','), _.trim);
            return rangevote
        }
        return rangevote
    };

    var rangevotes = Restangular.all('rangevotes');

    $scope.createRangevote = function (form) {
        var rangevote = $scope.convertRangeVote(form);
        if ($scope.rangevoteIsValid(rangevote)) {
            rangevotes.post(rangevote).then(function (newRangevote) {
                $location.path('/rangevotes/' + newRangevote.id + '/admin/');
            });
        }
    }
}]);

angular.module('rangevoting').controller('adminRangeVoteController', ['$scope', '$routeParams', 'Restangular', function ($scope, $routeParams, Restangular) {

    $scope.rangevote = Restangular.one("rangevotes", $routeParams.id).get().then(function (rangevote) {
        $scope.rangevote = rangevote;
    });

    $scope.addNewChoice = function (newChoice) {
        $scope.rangevote.choices.push(newChoice);
    };

    $scope.deleteChoice = function (choices, index) {
        choices.splice(index, 1);
    };

}]);