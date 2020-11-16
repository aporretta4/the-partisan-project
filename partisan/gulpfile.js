'use strict'

let fs = require('fs');
let gulp = require('gulp');
let gulputil = require('gulp-util');
let sass = require('gulp-sass');
let source = require('gulp-sourcemaps');
let autoprefixer = require('gulp-autoprefixer');
let globber = require('gulp-sass-glob')
let imagemin = require('gulp-imagemin');
let plumber = require('gulp-plumber');
let minify = require('gulp-minify');
let concat = require('gulp-concat');
let clean = require('gulp-clean');

gulp.task('buildSass', () => {
  return gulp.src('frontend/sass/**/*.scss')
    .pipe(plumber({
      errorHandler: (err) => {
        gulputil.beep();
        console.log(err.messageFormatted);
        this.emit('end');
      }
    }))
    .pipe(source.init({largeFile: true}))
    .pipe(globber())
    .pipe(sass())
    .pipe(autoprefixer())
    .pipe(source.write('maps'))
    .pipe(gulp.dest('static/css'));
});

gulp.task('removeNodePackageJs', (done) => {
  if (fs.existsSync('static/node_modules')) {
    return gulp.src('static/node_modules').pipe(clean());
  }
  else {
    done();
  }
});

gulp.task('removeJs', (done) => {
  if (fs.existsSync('static/js/scripts') && fs.existsSync('static/js/libraries')) {
    return gulp.src(['static/js/scripts', 'static/js/libraries']).pipe(clean());
  }
  else {
    done();
  }
});

gulp.task('createNodePackageJs', () => {
  return gulp.src([
      'node_modules/**/*.js',
      'node_modules/**/*/.min.js'
    ])
    .pipe(gulp.dest('static/node_modules'));
});

gulp.task('createJsLibs', () => {
  return gulp.src('frontend/js/libraries/**/*.js')
    .pipe(minify({
      'noSource': true,
      'ext': {
        'min': '.js'
      }
    }))
    .pipe(gulp.dest('static/js/libraries'));
});

gulp.task('createJsScripts', () => {
  return gulp.src('frontend/js/scripts/**/*.js')
    .pipe(concat('scripts.js'))
    .pipe(minify())
    .pipe(gulp.dest('static/js/scripts'));
});

gulp.task('buildJs', gulp.series('removeJs', 'createJsLibs', 'createJsScripts'));

gulp.task('buildImg', () => {
  return gulp.src('frontend/img/**/*')
    .pipe(imagemin())
    .pipe(gulp.dest('static/img'));
});

gulp.task('buildFonts', () => {
  return gulp.src([
    'frontend/fonts/**/*.otf',
    'frontend/fonts/**/*.ttf',
    'frontend/fonts/**/*.svg',
    'frontend/fonts/**/*.eot',
    'frontend/fonts/**/*.woff',
    'frontend/fonts/**/*.woff2',
    'frontend/fonts/**/*.css', // Automatic generation of css by some font services. Makes things convenient.
  ])
  .pipe(gulp.dest('static/fonts'));
})

gulp.task('watch', () => {
  gulp.watch('frontend/sass/**/*.scss', gulp.series('buildSass'));
  gulp.watch(['node_modules/**/*.js', 'node_modules/**/*/.min.js'], gulp.series('removeNodePackageJs', 'createNodePackageJs'));
  gulp.watch('frontend/js/**/*.js', gulp.series('removeJs', 'buildJs'));
  gulp.watch('frontend/img/**/*', gulp.series('buildImg'));
  gulp.watch('frontend/fonts/**/*', gulp.series('buildFonts'));
});

gulp.task('build',
  gulp.series(
    gulp.parallel(
      'buildSass',
      gulp.series('removeNodePackageJs','createNodePackageJs'),
      gulp.series('removeJs', 'buildJs'),
      'buildImg',
      'buildFonts'
    ), (done) => {
      done();
    }
  )
);
