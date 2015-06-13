var assert = chai.assert;

describe("create RangeVote Controller", function () {

    beforeEach(module('rangevoting'));

    var $scope, controller, rangevotes, httpBackend;

    beforeEach(inject(function ($rootScope, $controller, $httpBackend) {
        httpBackend = $httpBackend;
        $scope = $rootScope.$new();
        controller = $controller('createRangeVoteController', {$scope: $scope});
    }));

    beforeEach(function () {
        rangevotes = [{'question': 'Q1?'}, {'question': 'Q1?'}];
        httpBackend.expectGET('/rangevotes').respond(200, rangevotes);
        httpBackend.flush();
    });

    it('should init last_rangevotes', function () {
        assert.equal(2, $scope.rangevotes.length);
    });

    it('should convert form into rangevote', function () {
        var rangevote = $scope.convertRangeVote({question: 'Q?', choices: 'c1 ,c2, c3'});
        assert.equal('Q?', rangevote.question);
        assert.deepEqual(['c1', 'c2', 'c3'], rangevote.choices);
    });

    it('should convert undefined form into default rangevote', function () {
        var rangevote = $scope.convertRangeVote();
        assert.deepEqual({question: '', choices: []}, rangevote);
    });

    it('should convert undefined choices into default rangevote', function () {
        var rangevote = $scope.convertRangeVote({question: 'Q?'});
        assert.deepEqual({question: '', choices: []}, rangevote);
    });

    it('rangevote is valid if there is one question and two choices', function () {
        assert.ok($scope.rangevoteIsValid({
            question: 'New question ?',
            choices: ['first choice', 'second choice']
        }));
    });

    it('rangevote is invalid if there is no comma in form.choices', function () {
        assert.notOk($scope.rangevoteIsValid({
            question: 'New question ?',
            choices: ['first choice second choice']
        }));
    });

    it('rangevote is invalid if there is no form.question', function () {
        assert.notOk($scope.rangevoteIsValid({
            question: '',
            choices: ['first choice', 'second choice']
        }));
    });

});


describe("admin RangeVote Controller", function () {

    beforeEach(module('rangevoting'));

    var $scope, controller, httpBackend, rangevote, results;

    beforeEach(inject(function ($rootScope, $controller, $httpBackend) {
        httpBackend = $httpBackend;
        $scope = $rootScope.$new();
        controller = $controller('adminRangeVoteController', {$scope: $scope, $routeParams: {id: '375ce742-495f-4b0c-b831-3fb0dcc61b17'}});
    }));

    beforeEach(function () {
        rangevote = {"choices": ["c1", "c2"], "id": "375ce742-495f-4b0c-b831-3fb0dcc61b17", "question": "Q?", "votes": []};
        httpBackend.expectGET('/rangevotes/375ce742-495f-4b0c-b831-3fb0dcc61b17').respond(200, rangevote);
        results = {"ranking": [{"choice": "c1", "score": 0}, {"choice": "c2", "score": 0}], "answers": ["c1", "c2"], "question": "Q?", "number_of_votes": 0}
        httpBackend.expectGET('/rangevotes/375ce742-495f-4b0c-b831-3fb0dcc61b17/results').respond(200, results);
        httpBackend.flush();
    });

    it('should init rangevote id with routeParams id', function () {
        assert.equal('375ce742-495f-4b0c-b831-3fb0dcc61b17', $scope.rangevote.id);
    });

    it('should add a new choice', function () {
        $scope.newChoice = 'c3';
        $scope.addNewChoice();
        assert.deepEqual(['c1', 'c2', 'c3'], $scope.rangevote.choices);
        assert.equal('', $scope.newChoice)
    });

    it('should delete choice', function () {
        var firstChoice = 'c1';
        $scope.rangevote.choices = [firstChoice, 'c2', firstChoice];
        $scope.deleteChoice($scope.rangevote.choices, 0);
        assert.deepEqual(['c2', firstChoice], $scope.rangevote.choices);
    });

    it('should update vote with new value when update method is called', function (done) {
        httpBackend.whenPUT('/rangevotes/375ce742-495f-4b0c-b831-3fb0dcc61b17').respond(function () {
            done();
        });
        $scope.updateRangeVote();
        httpBackend.flush();
    })

});


describe("vote RangeVote Controller", function () {

    beforeEach(module('rangevoting'));

    var $scope, controller, httpBackend, rangevote;

    beforeEach(inject(function ($rootScope, $controller, $httpBackend) {
        httpBackend = $httpBackend;
        $scope = $rootScope.$new();
        controller = $controller('rangeVoteController', {$scope: $scope, $routeParams: {id: '375ce742-495f-4b0c-b831-3fb0dcc61b17'}});
    }));

    beforeEach(function () {
        rangevote = {"choices": ["c1", "c2"], "id": "375ce742-495f-4b0c-b831-3fb0dcc61b17", "question": "Q?", "votes": []};
        httpBackend.expectGET('/rangevotes/375ce742-495f-4b0c-b831-3fb0dcc61b17').respond(200, rangevote);
        httpBackend.flush();
    });

    it('should watch the opinion to fix the range input value', function () {
        $scope.vote = {
            elector: ""
        };

        $scope.$digest();

        assert.deepEqual(undefined, $scope.vote.opinions);

        $scope.vote = {
            elector: "",
            opinions: {'a a': "2", 'b': "-2"}
        };

        $scope.$digest();

        assert.deepEqual({'a a': 2, 'b': -2}, $scope.vote.opinions);
    });

    it('should contain a empty vote with opinions', function () {
        var expected_vote = {
            elector: "",
            opinions: {'c1': 0, 'c2': 0}
        };
        assert.equal(expected_vote.elector, $scope.vote.elector);
        assert.deepEqual(expected_vote.opinions, $scope.vote.opinions);
    });

    it('should POST new vote when create new vote method is called', function (done) {
        httpBackend.whenPOST('/rangevotes/375ce742-495f-4b0c-b831-3fb0dcc61b17/votes').respond(function () {
            done();
        });
        $scope.createNewVote();
        httpBackend.flush();
    });

});