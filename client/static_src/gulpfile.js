'use strict';

var gulp = require('gulp');
var uglify = require('gulp-uglify');
var del = require('del');
var concat = require('gulp-concat');
var autoprefixer = require('gulp-autoprefixer');
var minifycss = require('gulp-minify-css');

var sources = {
    img: 'img/**/*',
    js: [
        'bower_components/jquery/dist/jquery.js',
        'bower_components/html5sortable/jquery.sortable.js'
    ],
    css: [
        'css/base.css',
        'css/grids.css',
        'css/forms.css',
        'css/buttons.css'
    ]
};

var build_path = '../static';
var destination = {
    all: build_path + '/**',
    img: build_path + '/img',
    css: build_path + '/css',
    js: build_path + '/js'
};

var application_name = 'rangevoting';

gulp.task('images', function () {
    return gulp.src(sources.img)
        .pipe(gulp.dest(destination.img));
});

gulp.task('scripts', function () {
    return gulp.src(sources.js)
        .pipe(uglify())
        .pipe(concat(application_name + '.min.js'))
        .pipe(gulp.dest(destination.js));
});

gulp.task('css', function () {
    return gulp.src(sources.css)
        .pipe(concat(application_name + '.min.css'))
        .pipe(autoprefixer('last 3 version'))
        .pipe(minifycss())
        .pipe(gulp.dest(destination.css));
});

gulp.task('clean', function (callback) {
    del(destination.all, {force: true}, callback);
});

gulp.task('build', ['clean'], function () {
    gulp.start('scripts', 'css', 'images');
});

gulp.task('watch', ['build'], function () {
    gulp.watch(sources.css, ['css']);
    gulp.watch(sources.js, ['scripts']);
    gulp.watch(sources.img, ['images']);
});


gulp.task('default', ['build'], function () {

});