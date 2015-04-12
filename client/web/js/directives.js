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

angular.module('rangevoting').directive("contenteditable", function() {
  return {
    require: "ngModel",
    link: function(scope, element, attrs, ngModel) {

      function read() {
        ngModel.$setViewValue(element.html());
      }

      ngModel.$render = function() {
        element.html(ngModel.$viewValue || "");
      };

      element.bind("blur keyup change", function() {
        scope.$apply(read);
      });
    }
  };
});