'use strict';

var gulp = require('gulp');
var uglify = require('gulp-uglify');
var del = require('del');
var concat = require('gulp-concat');
var autoprefixer = require('gulp-autoprefixer');
var minifycss = require('gulp-minify-css');
var sass = require('gulp-sass');

var sources = {
    pages: 'pages/**/*',
    img: 'img/**/*',
    fonts: 'bower_components/font-awesome/fonts/**/*',
    js: [
        'bower_components/simple-notify/js/notification.js',
        'bower_components/angular/angular.js',
        'bower_components/angular-route/angular-route.js',
        'bower_components/lodash/lodash.js',
        'bower_components/restangular/dist/restangular.js',
        'js/rangevoting.js',
        'js/directives.js',
        'js/services.js',
        'js/controllers.js'
    ],
    scss: [
        'styles/**/*.scss'
    ]
};

var gulpSassOptions = {
    includePaths: ['bower_components/foundation/scss']
};

var build_path = '../static';
var destination = {
    all: build_path + '/**',
    pages: build_path + '/pages',
    img: build_path + '/img',
    css: build_path + '/css',
    js: build_path + '/js',
    fonts: build_path + '/fonts'
};

var application_name = 'rangevoting';

gulp.task('pages', function () {
    return gulp.src(sources.pages)
        .pipe(gulp.dest(destination.pages));
});


gulp.task('fonts', function () {
    return gulp.src(sources.fonts)
        .pipe(gulp.dest(destination.fonts));
});


gulp.task('images', function () {
    return gulp.src(sources.img)
        .pipe(gulp.dest(destination.img));
});

gulp.task('js', function () {
    return gulp.src(sources.js)
        .pipe(uglify())
        .pipe(concat(application_name + '.min.js'))
        .pipe(gulp.dest(destination.js));
});

gulp.task('scss', function () {
    return gulp.src(sources.scss)
        .pipe(sass(gulpSassOptions).on('error', sass.logError))
        .pipe(concat(application_name + '.min.css'))
        .pipe(autoprefixer('last 2 versions'))
        .pipe(minifycss({keepSpecialComments: 0}))
        .pipe(gulp.dest(destination.css));
});

gulp.task('clean', function (callback) {
    del(destination.all, {force: true}, callback);
});

gulp.task('build', ['clean'], function () {
    gulp.start('js', 'scss', 'images', 'pages', 'fonts');
});

gulp.task('watch', ['build'], function () {
    gulp.watch(sources.scss, ['scss']);
    gulp.watch(sources.js, ['js']);
    gulp.watch(sources.img, ['images']);
    gulp.watch(sources.pages, ['pages']);
});


gulp.task('default', ['build'], function () {

});