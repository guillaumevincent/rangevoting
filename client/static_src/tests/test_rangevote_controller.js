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

    it('rangevote is valid if there is one question and two choices', function () {
        assert.ok(scope.rangevoteIsValid({
            question: 'New question ?',
            choices: 'first choice,second choice'
        }));
    });

    it('rangevote is invalid if there is no comma in form.choices', function () {
        assert.notOk(scope.rangevoteIsValid({
            question: 'New question ?',
            choices: 'first choice second choice'
        }));
    });

    it('rangevote is invalid if there is no form.question', function () {
        assert.notOk(scope.rangevoteIsValid({
            question: '',
            choices: 'first choice,second choice'
        }));
    });

        it('rangevote is invalid if there is no form.question', function () {
        assert.notOk(scope.rangevoteIsValid());
    });

});