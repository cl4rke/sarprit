angular.module('SarpritApp', [], function($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
})
.controller('SarpritCtrl', ['$http', function ($http) {
	var Sarprit = this;
	Sarprit.loading = false;
	Sarprit.overallSentiment = 0;

	Sarprit.analyze = function (review) {
		Sarprit.sentences = []

		var sentences = review.match( /((#[\w^#]+ *)|([^\.!\?]+[\.!\?]* *))/g );

		Sarprit.loading = true;
		Sarprit.curLoaded = 0;
		Sarprit.maxLoaded = sentences.length * 3;
		Sarprit.overallSentiment = 0;

		for (var i = 0; i < sentences.length; i++) {
			Sarprit.sentences.push({value: sentences[i]});
		};

		for (var i = 0; i < Sarprit.sentences.length; i++) {
			$http.get('/classify/1/'+i+'/'+Sarprit.sentences[i].value).success(function (data) {
				Sarprit.sentences[data.id] = data;

				Sarprit.curLoaded++;

				$http.get('/classify/2/'+data.id+'/'+Sarprit.sentences[data.id].value).success(function (data) {
					Sarprit.sentences[data.id].clue = data.clue;
					Sarprit.sentences[data.id].clue_id = data.clue_id;

					Sarprit.curLoaded++;

					$http.get('/classify/3/'+Sarprit.sentences[data.id].clue.toLowerCase()[0]+'/'+data.id+'/'+Sarprit.sentences[data.id].value).success(function (data) {
						Sarprit.sentences[data.id].rating = data.rating;

						Sarprit.curLoaded++;

						if(Sarprit.curLoaded == Sarprit.maxLoaded) {
							var functional = 0;
							var humanic = 0;
							var mechanic = 0;
							var general = 0;

							for (var i = 0; i < Sarprit.sentences.length; i++) {
								sentence = Sarprit.sentences[i];

								if(sentence.clue_id == 0)
									functional += sentence.rating;
								else if(sentence.clue_id == 1)
									humanic += sentence.rating;
								else if(sentence.clue_id == 2)
									mechanic += sentence.rating;
								else if(sentence.clue_id == 3)
									general += sentence.rating;
							};

							functional /= Sarprit.sentences.length;
							humanic /= Sarprit.sentences.length;
							mechanic /= Sarprit.sentences.length;
							general /= Sarprit.sentences.length;

							$http.get('/classify/4/'+functional+'/'+humanic+'/'+mechanic+'/'+general).success(function (data) {
								Sarprit.overallSentiment = data.rating;
								Sarprit.loading = false;
							});
						}
					});
				});
			});
		};
	}

	Sarprit.range = function(n) {
        return new Array(n);
    };
}])
.controller('SurveyCtrl', ['$http', function ($http) {
	var survey = this;

	survey.review1 = '';
	survey.review2 = '';
	survey.review3 = '';
	survey.review4 = '';

	survey.sentences1 = [];
	survey.sentences2 = [];
	survey.sentences3 = [];
	survey.sentences4 = [];

	survey.overallRating1 = 0;
	survey.overallRating2 = 0;
	survey.overallRating3 = 0;
	survey.overallRating4 = 0;

	survey.splitReviews = function() {
		var sentence1 = survey.review1;
		var sentence2 = survey.review2;
		var sentence3 = survey.review3? survey.review3 : "";
		var sentence4 = survey.review4? survey.review4 : "";

		var result1 = sentence1.match( /((#[\w^#]+ *)|([^\.!\?]+[\.!\?]* *))/g );
		var result2 = sentence2.match( /((#[\w^#]+ *)|([^\.!\?]+[\.!\?]* *))/g );
		var result3 = sentence3.match( /((#[\w^#]+ *)|([^\.!\?]+[\.!\?]* *))/g );
		var result4 = sentence4.match( /((#[\w^#]+ *)|([^\.!\?]+[\.!\?]* *))/g );

		survey.sentences1 = [];
		survey.sentences2 = [];
		survey.sentences3 = [];
		survey.sentences4 = [];

		for (var i = 0; i < result1.length; i++) {
			survey.sentences1.push({value: result1[i], subjective: true, rating: 0});
		}
		for (var i = 0; i < result2.length; i++) {
			survey.sentences2.push({value: result2[i], subjective: true, rating: 0});
		}
		if (result3) {
			for (var i = 0; i < result3.length; i++) {
				survey.sentences3.push({value: result3[i], subjective: true, rating: 0});
			}
		}
		if (result4) {
			for (var i = 0; i < result4.length; i++) {
				survey.sentences4.push({value: result4[i], subjective: true, rating: 0});
			}
		}
	}

	survey.removeRatings = function (sentence) {
		if(sentence.subjective) {
			delete sentence.clue
			delete sentence.rating
			sentence.rating = 0;
		}
	}

	survey.step2ok = function () {
		for (var i = 0; i < survey.sentences1.length; i++) {
			sentence = survey.sentences1[i];
			if( ! sentence.value)
				return false;
		};

		for (var i = 0; i < survey.sentences2.length; i++) {
			sentence = survey.sentences2[i];
			if( ! sentence.value)
				return false;
		};

		for (var i = 0; i < survey.sentences3.length; i++) {
			sentence = survey.sentences3[i];
			if( ! sentence.value)
				return false;
		};

		for (var i = 0; i < survey.sentences4.length; i++) {
			sentence = survey.sentences4[i];
			if( ! sentence.value)
				return false;
		};

		return true;
	}
	survey.step3ok = function () {
		for (var i = 0; i < survey.sentences1.length; i++) {
			sentence = survey.sentences1[i];
			if(sentence.subjective && (!sentence.rating || !sentence.clue))
				return false;
		};

		for (var i = 0; i < survey.sentences2.length; i++) {
			sentence = survey.sentences2[i];
			if(sentence.subjective && (!sentence.rating || !sentence.clue))
				return false;
		};

		for (var i = 0; i < survey.sentences3.length; i++) {
			sentence = survey.sentences3[i];
			if(sentence.subjective && (!sentence.rating || !sentence.clue))
				return false;
		};

		for (var i = 0; i < survey.sentences4.length; i++) {
			sentence = survey.sentences4[i];
			if(sentence.subjective && (!sentence.rating || !sentence.clue))
				return false;
		};

		return true;
	}

	survey.step4ok = function () {

		if(survey.review1 && !survey.overallRating1)
			return false;
		if(survey.review2 && !survey.overallRating2)
			return false;
		if(survey.review3 && !survey.overallRating3)
			return false;
		if(survey.review4 && !survey.overallRating4)
			return false;

		return true;
	}
}])
.controller('StudentsCtrl', ['$http', '$interval', function ($http, $interval) {
	var students = this;
	students.value = [];

	students.refresh = function () {
		$http.get('/admin/data').success(function (data) {
			for (var i = 0; i < data.length; i++) {
				if(data[i].current) {
					students.value = data[i].students;
					break;
				}
			};
		});
	}

	$interval( function () {
		students.refresh();
	}, 10000);

	students.refresh();
}])
.controller('SystemCtrl', ['$http', function ($http) {
	var system = this;

	$http.get("api/data").success( function (data) {
		system.reviews = data.reviews;
		system.sentences = data.sentences;
	});
}])
.controller('TwitterCtrl', ['$http', function ($http) {
	var twitter = this;
}]);
