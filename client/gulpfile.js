'use strict';

var gulp = require('gulp');
var uglify = require('gulp-uglify');
var del = require('del');
var concat = require('gulp-concat');

var bower = {
    js: 'bower_components/jquery/dist/jquery.js'
};

var destination = 'static';
var application_name = 'rangevoting';

gulp.task('scripts', function () {
    return gulp.src(bower.js)
        .pipe(uglify())
        .pipe(concat(application_name + '.min.js'))
        .pipe(gulp.dest(destination + '/js'));
});


gulp.task('clean', function (callback) {
    del(destination + '/**', {force: true}, callback);
});

gulp.task('build', ['clean'], function () {
    gulp.start('scripts');
});


gulp.task('default', ['build'], function () {

});