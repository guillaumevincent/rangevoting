angular.module('rangevoting').factory('Url', ['$location', function ($location) {
    return {
        getBaseUrl: function () {
            var absoluteUrl = $location.absUrl();
            var relativeUrl = $location.url();
            return absoluteUrl.substring(0, absoluteUrl.length - relativeUrl.length);
        }
    }
}]);