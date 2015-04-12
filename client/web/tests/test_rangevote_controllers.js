var assert = chai.assert;

describe("create RangeVote Controller", function () {

    beforeEach(module('rangevoting'));

    var scope, controller;

    beforeEach(inject(function ($rootScope, $controller) {
        scope = $rootScope.$new();
        controller = $controller('createRangeVoteController', {$scope: scope});
    }));

    it('should convert form into rangevote', function () {
        var rangevote = scope.convertRangeVote({question: 'Q?', choices: 'c1 ,c2, c3'});
        assert.equal('Q?', rangevote.question);
        assert.deepEqual(['c1', 'c2', 'c3'], rangevote.choices);
    });

    it('should convert undefined form into default rangevote', function () {
        var rangevote = scope.convertRangeVote();
        assert.deepEqual({question: '', choices: []}, rangevote);
    });

    it('rangevote is valid if there is one question and two choices', function () {
        assert.ok(scope.rangevoteIsValid({
            question: 'New question ?',
            choices: ['first choice', 'second choice']
        }));
    });

    it('rangevote is invalid if there is no comma in form.choices', function () {
        assert.notOk(scope.rangevoteIsValid({
            question: 'New question ?',
            choices: ['first choice second choice']
        }));
    });

    it('rangevote is invalid if there is no form.question', function () {
        assert.notOk(scope.rangevoteIsValid({
            question: '',
            choices: ['first choice', 'second choice']
        }));
    });

});


describe("admin RangeVote Controller", function () {

    beforeEach(module('rangevoting'));

    var scope, controller, httpBackend;

    beforeEach(inject(function ($rootScope, $controller, $httpBackend) {
        httpBackend = $httpBackend;
        scope = $rootScope.$new();
        controller = $controller('adminRangeVoteController', {$scope: scope, $routeParams: {id: '375ce742-495f-4b0c-b831-3fb0dcc61b17'}});
    }));

    beforeEach(function () {
        var rangevote = {"choices": ["c1", "c2"], "id": "375ce742-495f-4b0c-b831-3fb0dcc61b17", "question": "Q?", "votes": []};
        httpBackend.expectGET('/rangevotes/375ce742-495f-4b0c-b831-3fb0dcc61b17').respond(200, rangevote);
        httpBackend.flush();
    });

    it('should init rangevote id with routeParams id', function () {
        assert.equal('375ce742-495f-4b0c-b831-3fb0dcc61b17', scope.rangevote.id);
    });

    it('should add a new choice', function () {
        scope.addNewChoice('c3');
        assert.deepEqual(['c1', 'c2', 'c3'], scope.rangevote.choices)
    });

    it('should delete choice', function () {
        var firstChoice = 'c1';
        scope.rangevote.choices = [firstChoice, 'c2', firstChoice];
        scope.deleteChoice(scope.rangevote.choices, 0);
        assert.deepEqual(['c2', firstChoice], scope.rangevote.choices);
    });
});