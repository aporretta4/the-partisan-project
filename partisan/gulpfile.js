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
let CacheBuster = require('gulp-cachebust');

let buster = new CacheBuster({
  'pathFormatter': (dirname, basename, extname, checksum) => {
    return require('path').join(dirname, basename + '___' + checksum + extname);
  }
});

gulp.task('gatherFileHashes', (done) => {
    return gulp.src('frontend/**/*.*').pipe(buster.resources());
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
  if (fs.existsSync('static/js')) {
    return gulp.src('static/js').pipe(clean());
  }
  else {
    done();
  }
});

gulp.task('removeCss', (done) => {
  if (fs.existsSync('static/css')) {
    return gulp.src(['static/css']).pipe(clean());
  }
  else {
    done();
  }
});

gulp.task('removeFonts', (done) => {
  if (fs.existsSync('static/fonts')) {
    return gulp.src(['static/fonts']).pipe(clean());
  }
  else {
    done();
  }
});

gulp.task('removeImgs', (done) => {
  if (fs.existsSync('static/img')) {
    return gulp.src(['static/img']).pipe(clean());
  }
  else {
    done();
  }
});

gulp.task('createSass', () => {
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
    .pipe(buster.resources())
    .pipe(buster.references())
    .pipe(gulp.dest('static/css'));
});

gulp.task('createChartJs', () => {
  return gulp.src('node_modules/chart.js/**/*.js')
    .pipe(buster.resources())
    .pipe(buster.references())
    .pipe(gulp.dest('static/node_modules/chart.js/'));
})

gulp.task('createJsLibs', () => {
  return gulp.src('frontend/js/libraries/**/*.js')
    .pipe(minify({
      'noSource': true,
      'ext': {
        'min': '.js'
      }
    }))
    .pipe(buster.resources())
    .pipe(buster.references())
    .pipe(gulp.dest('static/js/libraries'));
});

gulp.task('createJsScripts', () => {
  return gulp.src('frontend/js/scripts/**/*.js')
    .pipe(concat('scripts.js'))
    .pipe(minify())
    .pipe(buster.resources())
    .pipe(buster.references())
    .pipe(gulp.dest('static/js/scripts'));
});

gulp.task('createImgs', () => {
  return gulp.src('frontend/img/**/*')
    .pipe(buster.resources())
    .pipe(imagemin())
    .pipe(gulp.dest('static/img'));
});

gulp.task('createFonts', () => {
  return gulp.src([
    'frontend/fonts/**/*.otf',
    'frontend/fonts/**/*.ttf',
    'frontend/fonts/**/*.svg',
    'frontend/fonts/**/*.eot',
    'frontend/fonts/**/*.woff',
    'frontend/fonts/**/*.woff2',
  ])
  .pipe(buster.resources())
  .pipe(gulp.dest('static/fonts'));
});

gulp.task('buildFontCss', () => {
  return gulp.src([
    'frontend/fonts/**/*.css', // Automatic generation of css by some font services. Makes things convenient.
  ])
  .pipe(buster.resources())
  .pipe(buster.references())
  .pipe(gulp.dest('static/fonts'));
});

gulp.task('buildJs', gulp.series('removeJs', 'removeNodePackageJs', 'createChartJs', 'createJsLibs', 'createJsScripts'));
gulp.task('buildSass', gulp.series('removeCss', 'createSass'));
gulp.task('buildImg', gulp.series('removeImgs', 'createImgs'));
gulp.task('buildFonts', gulp.series('removeFonts', 'createFonts', 'buildFontCss'));

gulp.task('watch', () => {
  gulp.watch(['node_modules/**/*.js'], gulp.series('gatherFileHashes', 'buildJs'));
  gulp.watch('frontend/js/**/*.js', gulp.series('gatherFileHashes', 'buildJs'));
  gulp.watch('frontend/img/**/*', gulp.series('gatherFileHashes', 'buildImg', 'buildSass'));
  gulp.watch('frontend/fonts/**/*', gulp.series('gatherFileHashes', 'buildFonts', 'buildSass'));
  gulp.watch('frontend/sass/**/*.scss', gulp.series('gatherFileHashes', 'buildSass'));
});

gulp.task('build',
  gulp.series(
    'gatherFileHashes',
    'buildJs',
    'buildImg',
    'buildFonts',
    'buildSass',
    (done) => {
      done();
    }
  )
);
