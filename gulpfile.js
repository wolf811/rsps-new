'use strict';
// var gulp = require('gulp');
// var bs = require('browser-sync').create();
// var sass = require('gulp-sass');
// var autoprefixer = require('gulp-autoprefixer');
// var wait = require('gulp-wait')

// gulp.task('browser-sync', ['sass'], function () {
//     bs.init({
//         server: {
//             baseDir: "./"
//         }
//     });
// });

// gulp.task('sass', function(){
//     return gulp.src('scss/*.scss')
//         .pipe(wait(500))
//         .pipe(sass({errLogToConsole: true}))
//         .pipe(autoprefixer({browsers: ['last 2 versions'], cascade: false}))
//         .pipe(gulp.dest('css/'))
//         .pipe(bs.reload({stream: true}));
// });

// gulp.task('watch', ['browser-sync'], function() {
//     gulp.watch("scss/*.scss", ['sass']);
//     gulp.watch("*.html").on('change', bs.reload);
//     gulp.watch("includes/*.html").on('change', bs.reload);
// })

var gulp = require('gulp');
var sass = require('gulp-sass');
var bs = require('browser-sync').create();
var wait = require('gulp-wait');
var exec = require('child_process').exec;

gulp.task('browser-sync', ['runserver'], function() {
    bs.init({
      notify: true,
      port: 8000,
      proxy: 'localhost:8000',
      // ws: true
    })
  });

gulp.task('runserver', function() {
    var proc = exec('python manage.py runserver')
  })

gulp.task('sass', function(){
    return gulp.src('assets/scss/*.scss')
        .pipe(wait(500))
        .pipe(sass())
        .pipe(gulp.dest('static/css/'))
        .pipe(bs.reload({stream: true}));
});

gulp.task('watch', ['browser-sync', 'sass'], function() {
    gulp.watch("assets/scss/*.scss", ['sass']);
    gulp.watch("static/js/*.js").on('change', bs.reload);
    gulp.watch("**/templates/**/*.html").on('change', bs.reload);
})