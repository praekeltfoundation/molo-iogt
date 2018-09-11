'use strict';

var gulp              =   require('gulp'),
    sass              =   require('gulp-sass'),
    watch             =   require('gulp-watch'),
    cleanCSSMinify    =   require('gulp-clean-css'),
    rename            =   require('gulp-rename'),
    gzip              =   require('gulp-gzip'),
    notify            =   require('gulp-notify'),
    sourcemaps        =   require('gulp-sourcemaps'),
    livereload        =   require('gulp-livereload');

var sassPaths = [
    'iogt/styles/iogt/opera-mini_single-view.scss',
    'iogt/styles/iogt/style-rtl.scss',
    'iogt/styles/iogt/style.scss',
    'iogt/styles/iogt/state_320/state_320.scss',
    'iogt/styles/iogt/maintenance.scss',
];

var sassDest = {
     prd: 'iogt/static/css/prd',
     dev: 'iogt/static/css/dev'
};


function styles(env) {
  var s = gulp.src(sassPaths);
  var isDev = env === 'dev';

  if (isDev) s = s
    .pipe(sourcemaps.init());

    s = s
    .pipe(sass().on('error', sass.logError))
    .pipe(cleanCSSMinify())
    if (isDev) s = s
        .pipe(sourcemaps.write('/maps'));
        return s
        .pipe(gulp.dest(sassDest[env]))
        .pipe(notify({ message: `Styles task complete: ${env}` }));
}

gulp.task('styles:prd', function() {
  return styles('prd');
});

gulp.task('styles:dev', function() {
  return styles('dev');
});

gulp.task('watch', function() {
    livereload.listen();
    gulp.watch('iogt/styles/iogt/**/*.scss', ['styles']);
});

gulp.task('styles', ['styles:dev', 'styles:prd']);
gulp.task('default', ['styles']);
