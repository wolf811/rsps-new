'use strict';

var gulp = require('gulp');
var sass = require('gulp-sass');
var autoprefixer = require('gulp-autoprefixer');
var bs = require('browser-sync').create();
var wait = require('gulp-wait');
var exec = require('child_process').exec;

gulp.task('browser-sync', ['runserver'], function() {
    bs.init({
      notify: true,
      port: 8000,
      proxy: 'localhost:8000',
    })
  });

gulp.task('runserver', function() {
    var proc = exec('python manage.py runserver')
  })

gulp.task('sass', function(){
    return gulp.src('assets/scss/*.scss')
        .pipe(wait(500))
        .pipe(sass({errLogToConsole: true}))
        .pipe(autoprefixer({browsers: ['last 2 versions'], cascade: false}))
        .pipe(gulp.dest('static/css/'))
        .pipe(bs.reload({stream: true}));
});

gulp.task('watch', ['browser-sync', 'sass'], function() {
    gulp.watch("assets/scss/*.scss", ['sass']);
    gulp.watch("static/js/*.js").on('change', bs.reload);
    gulp.watch("**/templates/**/*.html").on('change', bs.reload);
})