angular.module('rangevoting').directive('haschoices', function () {
    return {
        require: 'ngModel',
        link: function (scope, elm, attrs, ctrl) {
            ctrl.$validators.haschoices = function (modelValue, viewValue) {
                if (viewValue) {
                    var choices = viewValue.split(',').filter(Boolean);
                    if (choices.length > 1) {
                        return true;
                    }
                }
                return false;
            };
        }
    };
});

angular.module('rangevoting').directive('autofocus', function () {
    return {
        restrict: 'A',
        link: function ($scope, element, attrs) {
            element[0].focus();
        }
    };
});


angular.module('rangevoting').directive('share', function () {

    var controller = ['$scope', function ($scope) {
        $scope.getTwitterUrl = function () {
            return "https://twitter.com/home?status=" + encodeURIComponent($scope.message);
        };
        $scope.getFacebookUrl = function () {
            return "https://www.facebook.com/sharer/sharer.php?u=" + encodeURIComponent($scope.message);
        };
        $scope.getGooglePlusUrl = function () {
            return "https://plus.google.com/share?url=" + encodeURIComponent($scope.url);
        };
    }];

    return {
        restrict: 'E',
        scope: {
            message: '=message',
            url: '=url'
        },
        controller: controller,
        templateUrl: 'static/pages/share.html'
    };
});

angular.module('rangevoting').directive('selectOnClick', function () {
    return {
        restrict: 'A',
        link: function (scope, element, attrs) {
            element.on('click', function () {
                this.select();
            });
        }
    };
});