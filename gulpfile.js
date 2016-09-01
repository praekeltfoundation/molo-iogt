var gulp        =   require('gulp'), 
    sass        =   require('gulp-sass'), 
    watch       =   require('gulp-watch'), 
    minifycss   =   require('gulp-minify-css'),
    rename      =   require('gulp-rename'),
    gzip        =   require('gulp-gzip'),
    notify      =   require('gulp-notify'),
    livereload  =   require('gulp-livereload');

var gzip_options = {
    threshold: '1kb',
    gzipOptions: {
        level: 9
    }
};

gulp.task('styles', function() {
    return gulp.src('iogt/static/css/*.scss')
        .pipe(sass())
        .pipe(rename({suffix: '.min'}))
        .pipe(minifycss())
        .pipe(gulp.dest('iogt/static/css/dest'))
        .pipe(gzip(gzip_options))
        .pipe(gulp.dest('iogt/static/css/dest'))
        .pipe(notify({ message: 'Styles task complete' }))
        .pipe(livereload());
});
gulp.task('watch', function() {
    livereload.listen();
    gulp.watch('iogt/static/css/*.scss/**.scss', ['styles']);
});
gulp.task('default', ['styles', 'watch']);