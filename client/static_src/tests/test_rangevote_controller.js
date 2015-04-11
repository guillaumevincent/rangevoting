var assert = chai.assert;

describe("create RangeVote Controller", function () {

    beforeEach(module('rangevoting'));

    var scope, controller;

    beforeEach(inject(function ($rootScope, $controller) {
        scope = $rootScope.$new();
        controller = $controller('createRangeVoteController', {$scope: scope});
    }));

    it('rangevote object is properly initialized', function () {
        assert.equal(scope.rangevote.question, '');
        assert.deepEqual(scope.rangevote.choices, []);
    });
});