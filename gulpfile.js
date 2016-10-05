'use strict';

var gulp        =   require('gulp'), 
    sass        =   require('gulp-sass'), 
    watch       =   require('gulp-watch'), 
    minifycss   =   require('gulp-minify-css'),
    rename      =   require('gulp-rename'),
    gzip        =   require('gulp-gzip'),
    notify      =   require('gulp-notify'),
    sourcemaps  =   require('gulp-sourcemaps'),
    sassdoc     =   require('sassdoc'),
    livereload  =   require('gulp-livereload'),
    scss_destination = 'iogt/static/css/dest';

var sass_paths = [
        'iogt/static/css/opera-mini_single-view.scss',
        'iogt/static/css/style-rtl.scss',
        'iogt/static/css/style.scss',
        'iogt/static/css/state_320/state_320.scss',
        'iogt/static/css/versions.scss'
    ];

gulp.task('styles', function() {
    return gulp.src(sass_paths)
    .pipe(sourcemaps.init())
    .pipe(sass().on('error', sass.logError))
    .pipe(rename({suffix: '.min'}))
    .pipe(minifycss())
    .pipe(sourcemaps.write('/maps'))
    .pipe(gulp.dest(scss_destination))
    .pipe(notify({ message: 'Styles task complete' }));
});

gulp.task('sassdoc', function() {
    return  gulp.src('iogt/static/css/styles.scss')
        .pipe(sassdoc('iogt/static/documentation'))
        .resume();
});

gulp.task('watch', function() {
    livereload.listen();
    gulp.watch('iogt/static/css/*.scss', ['styles']);
});

gulp.task('default', ['styles']);