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

    scss_inputs = 'iogt/static/css/*.scss',
    scss_destination = 'iogt/static/css/dest';

gulp.task('styles', function() {
    return gulp.src(scss_inputs)
        .pipe(sass())
        .pipe(sourcemaps.init())
        .pipe(rename({suffix: '.min'}))
        .pipe(minifycss())
        .pipe(gulp.dest(scss_destination))
        .pipe(sourcemaps.write('iogt/static/maps'))
        .pipe(gulp.dest(scss_destination))
        .pipe(notify({ message: 'Styles task complete' }))
        .pipe(livereload());
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

gulp.task('default', ['styles', 'watch','sassdoc']);