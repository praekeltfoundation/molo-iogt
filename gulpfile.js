var gulp        =   require('gulp'), 
    sass        =   require('gulp-sass'), 
    watch       =   require('gulp-watch'), 
    minifycss   =   require('gulp-minify-css'),
    rename      =   require('gulp-rename'),
    gzip        =   require('gulp-gzip'),
    notify      =   require('gulp-notify'),
    sourcemaps  =   require('gulp-sourcemaps'),
    livereload  =   require('gulp-livereload');
/*var gzip_options = {
    threshold: '1kb',
    gzipOptions: {
        level: 9
    }
};*/

var scss_inputs = 'iogt/static/css/*.scss',
    scss_destination = 'iogt/static/css/dest';
gulp.task('styles', function() {
    return gulp.src(scss_inputs)
        .pipe(sass())
        .pipe(rename({suffix: '.min'}))
        .pipe(minifycss())
        .pipe(gulp.dest(scss_destination))
        .pipe(sourcemaps.write('iogt/static/maps'))
        .pipe(gulp.dest(scss_destination))
        .pipe(notify({ message: 'Styles task complete' }))
        .pipe(livereload());
});
gulp.task('watch', function() {
    livereload.listen();
    gulp.watch('iogt/static/css/*.scss/**.scss', ['styles']);
});
gulp.task('default', ['styles', 'watch']);