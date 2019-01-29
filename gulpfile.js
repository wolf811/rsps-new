'use strict';
var gulp = require('gulp');
var bs = require('browser-sync').create();
var sass = require('gulp-sass');
var autoprefixer = require('gulp-autoprefixer');
var wait = require('gulp-wait')

gulp.task('browser-sync', ['sass'], function () {
    bs.init({
        server: {
            baseDir: "./"
        }
    });
});

gulp.task('sass', function(){
    return gulp.src('scss/*.scss')
        .pipe(wait(500))
        .pipe(sass({errLogToConsole: true}))
        .pipe(autoprefixer({browsers: ['last 2 versions'], cascade: false}))
        .pipe(gulp.dest('css/'))
        .pipe(bs.reload({stream: true}));
});

gulp.task('watch', ['browser-sync'], function() {
    gulp.watch("scss/*.scss", ['sass']);
    gulp.watch("*.html").on('change', bs.reload);
    gulp.watch("includes/*.html").on('change', bs.reload);
})