angular.module('rangevoting').controller('createRangeVoteController', ['$scope', 'Url', 'Restangular', function ($scope, Url, Restangular) {
    $scope.iNeedSomeHelp = false;

    $scope.rangevoteIsValid = function (rangevote) {
        return !!(rangevote.question && rangevote.choices.length > 1);
    };

    $scope.convertRangeVote = function (form) {
        var rangevote = {question: '', choices: []};
        if (form && form.question && form.choices) {
            rangevote.question = form.question;
            rangevote.choices = _.map(form.choices.split(','), _.trim);
            return rangevote
        }
        return rangevote
    };

    var rangevotes = Restangular.all('rangevotes');

    $scope.createRangeVote = function (form) {
        var rangevote = $scope.convertRangeVote(form);
        if ($scope.rangevoteIsValid(rangevote)) {
            rangevotes.post(rangevote).then(function (newRangevote) {
                Url.redirect('/rangevotes/' + newRangevote.id + '/admin/');
            });
        }
    }
}]);

angular.module('rangevoting').controller('adminRangeVoteController', ['$scope', '$routeParams', 'Url', 'Restangular', function ($scope, $routeParams, Url, Restangular) {

    $scope.rangevote_id = $routeParams.id;

    $scope.rangevote = Restangular.one("rangevotes", $routeParams.id).get().then(function (rangevote) {
        $scope.rangevote = rangevote;
        $scope.rangevote_url = Url.getBaseUrl() + '/rangevotes/' + $routeParams.id;
        $scope.message_to_share = rangevote.question + ' ' + $scope.rangevote_url + ' #votedevaleur';
    });

    $scope.newChoice = '';
    $scope.addNewChoice = function () {
        $scope.rangevote.choices.push($scope.newChoice);
        $scope.newChoice = '';
    };

    $scope.deleteChoice = function (choices, index) {
        choices.splice(index, 1);
    };

    $scope.updateRangeVote = function () {
        $scope.rangevote.put().then(function () {
            new Notification({
                message: '<p>votre vote a été correctement mis à jour.</p>',
                ttl: 5000,
                type: 'success'
            }).show();
        }, function () {
            new Notification({
                message: "<p>Je suis désolé, quelque chose a mal tourné. Pouvez-vous me dire comment cela est arrivé par <a href='mailto:contact@oslab.fr?subject=Erreur vote de valeur'>e-mail</a> ?<br/>Je tiens à corriger le problème pour que cela ne se reproduise pas.</p>",
                ttl: 20000,
                type: 'error'
            }).show();
        });
    };
}]);


angular.module('rangevoting').controller('rangeVoteController', ['$scope', '$routeParams', 'Url', 'Restangular', function ($scope, $routeParams, Url, Restangular) {
    $scope.vote = {
        elector: ''
    };

    $scope.initVote = function (choices) {
        var opinions = {};
        for (var i = 0; i < choices.length; i++) {
            opinions[choices[i]] = 0;
        }
        $scope.vote = {
            elector: '',
            opinions: opinions
        };
    };

    $scope.rangevote = Restangular.one("rangevotes", $routeParams.id).get().then(function (rangevote) {
        $scope.rangevote = rangevote;
        $scope.initVote(rangevote.choices);
        $scope.rangevote_url = Url.getBaseUrl() + '/rangevotes/' + $routeParams.id;
        $scope.message_to_share = rangevote.question + ' ' + $scope.rangevote_url + ' #votedevaleur';
    });

    $scope.$watch('vote', function (newVote, oldVote) {
        if (typeof(newVote.opinions) !== 'undefined') {
            var opinions = $scope.vote.opinions;
            for (var key in  opinions) {
                if (opinions.hasOwnProperty(key)) {
                    opinions[key] = parseInt(opinions[key]);
                }
            }
        }
    }, true);

    $scope.createNewVote = function () {
        $scope.rangevote.all('votes').post($scope.vote).then(function () {
            $scope.showResults();
        }, function () {
            new Notification({
                message: "<p>Je suis désolé, quelque chose a mal tourné. Pouvez-vous me dire comment cela est arrivé par <a href='mailto:contact@oslab.fr?subject=Erreur vote de valeur'>e-mail</a> ?<br/>Je tiens à corriger le problème pour que cela ne se reproduise pas.</p>",
                ttl: 20000,
                type: 'error'
            }).show();
        });
    };

    $scope.showResults = function () {
        Url.redirect('/rangevotes/' + $routeParams.id + '/results/');
    };
}]);


angular.module('rangevoting').controller('resultRangeVoteController', ['$scope', '$routeParams', 'Restangular', function ($scope, $routeParams, Restangular) {

}]);

