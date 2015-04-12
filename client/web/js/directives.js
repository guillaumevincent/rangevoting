angular.module('rangevoting').directive('haschoices', function () {
    return {
        require: 'ngModel',
        link: function (scope, elm, attrs, ctrl) {
            ctrl.$validators.haschoices = function (modelValue, viewValue) {
                if (viewValue) {
                    var choices = viewValue.split(',');
                    if (choices.length > 1) {
                        return true;
                    }
                }
                return false;
            };
        }
    };
});