# lektor-gulp-support

Adds gulp support to lektor .

This is a plugin is a port of lekto-webpack-support for Lektor that adds support
 for gulp to projects.  When enabled it can build a gulp project from the `gulp/` folder into the
asset folder automatically when the server (or build task) is run with
the `-f gulp` flag.

## Enabling the Plugin

To enable the plugin add this to your project file, run this command while
sitting in your Lektor project directory:

```bash
lektor plugins add lektor-gulp-support
```

## Creating a Gulp Project

Next you need to create a gulp project. Create a `gulp/` folder and
inside that folder create `package.json` and a `gulpfile.js`

### `gulp/package.json`

This file instructs `npm` which packages we will need.  All we need for a
start is to create an almost empty file (name and version fields are mandatory
but not important for functionality, change them to suit your own needs):

```json
{
  "name": "lektor-gulp",
  "version": "1.0.0",
  "private": true
}
```

Now we can `npm install` (or `yarn add`) the rest:

>  I use Gulp 4 for this

```bash
$ cd </path/to/your/lektor/project>/gulp
$ npm install --save-dev 'gulpjs/gulp#4.0' gulp-load-plugins gulp-babel gulp-reporter gulp-uglify gulp-rename gulp-sass gulp-csscomb gulp-postcss gulp-cssimport gulp-cssnano gulp-cached gulp-imagemin
$ npm install --save-dev postcss-import postcss-flexbugs-fixes postcss-reporter postcss-merge-rules postcss-sorting css-mqpacker stylelint autoprefixer del
```

This will install gulp4.0 itself together with babel, sass and postcss as well as
a bunch of loaders we need for getting all that configured.  Because we
created a `package.json` before and we use `--save-dev` the dependencies
will be remembered in the `package.json` file.

### `gulp/gulpfile.js`

Next up is the gulp config file.  Here we will go with a very basic
setup that's good enough to cover most things you will encounter.  The
idea is to build the files from `gulp/src` into
`assets/static` so that we can use it even if we do not have gulp
installed for as long as someone else ran it before.

```javascript
var gulp = require('gulp')
var path = require('path')
var del = require('del')
var browserSync = require('browser-sync')
var $ = require('gulp-load-plugins')()

var processors = [
  require('postcss-import')(),
  require('postcss-flexbugs-fixes'),
  require('css-mqpacker')({
    sort: true
  }),
  require('postcss-merge-rules'),
  require('postcss-sorting')({ /* sorting options */ }),
  require('stylelint'),
  require('postcss-reporter')({
    clearReportedMessages: true
  })
]

var autoprefixer = [
  require('autoprefixer')({
    browsers: [
      'last 2 versions',
      'Explorer >= 8'
    ]
  })
]

var entries = './src' // entries directory
var output = path.dirname(__dirname) + '/assets/static/dist' // output directory

var paths = {
  styles: {
    src: entries + '/scss/**/*.scss',
    dest: output + '/css'
  },
  scripts: {
    src: entries + '/js/**/*.js',
    dest: output + '/js'
  },
  fonts: {
    src: entries + '/fonts/**/*.+(woff2?|ttf|eot|otf|svg)',
    dest: output + '/fonts'
  },
  images: {
    src: entries + '/images/**/*.+(png|jpe?g|gif|svg)',
    dest: output + '/images'
  }
}

// build js files into es2015 and create minify version
gulp.task('scripts', function (done) {
  gulp.src([paths.scripts.src, '!node_modules/**'], {
      sourcemaps: true
    })
    .pipe($.babel({
      presets: ['env'],
      plugins: ['babel-polyfill']
    }))
    .pipe($.eslint())
    .pipe($.eslint.format())
    // .pipe($.eslint.failAfterError())
    .pipe($.reporter({ /* reporter options */ }))
    .pipe(gulp.dest(paths.scripts.dest))
    // minify js
    .pipe($.uglify())
    .pipe($.rename({
      basename: 'app',
      suffix: '.min'
    }))
    .pipe(gulp.dest(paths.scripts.dest))
  done()
})


// build scss files into css and create minify version
gulp.task('styles', function (callback) {
  gulp.src(paths.styles.src, {
      sourcemaps: true
    })
    .pipe($.sass().on('error', $.sass.logError))
    .pipe($.csscomb())
    .pipe($.postcss(processors))
    .pipe($.cssimport({ /* cssimport options */ }))
    .pipe(gulp.dest(paths.styles.dest))
    // prefix and minify css
    .pipe($.postcss(autoprefixer))
    .pipe($.cssnano())
    .pipe($.rename({
      basename: 'main',
      suffix: '.min'
    }))
    .pipe(gulp.dest(paths.styles.dest))
  callback()
})

// optimize images and set them in the cache
gulp.task('images', function (done) {
  gulp.src(paths.images.src)
    .pipe($.cached(
      $.imagemin({
        interlaced: true,
        progressive: true,
        optimizationLevel: 5
      })
    ))
    .pipe(gulp.dest(paths.images.dest))
  done()
})

// copy local font to output
gulp.task('fonts', function (done) {
  gulp.src(paths.fonts.src)
    .pipe(gulp.dest(paths.fonts.dest))
  done()
})

// clean previws build
gulp.task('clean:build', function (callback) {
  del.sync([output], {
    force: true
  })
  callback()
})

// clear cache
gulp.task('clean:cache', function (done) {
  $.cached.caches = {}
  done()
})

// build parallel task
gulp.task('clean', gulp.parallel('clean:build', 'clean:cache'))
gulp.task('common', gulp.parallel('images', 'fonts'))

// [required] defauld task
// `lektor build -f gulp` will execute this task
gulp.task('default', gulp.series('clean', gulp.parallel('scripts', 'styles', 'common')))

// [required] task name must be 'watch'
// `lektor server -f gulp` will execute this task
gulp.task('watch', function () {
  gulp.watch(paths.styles.src, gulp.series('clean', gulp.parallel('styles', 'common')))
  gulp.watch(paths.scripts.src, gulp.series('scripts'))
})
```

## Creating the App

Now we can start building our app.  We configured at least two files
in gulp: `src/js/app.js` and `src/scss/main.scss`.  Those are the entry
points we need to have.

## Running the Server
> #### notice!
> to run `lektor server -f gulp` you must have a task called `watch` in your gulpfile.js.

Now you're ready to go.  When you run `lektor server` gulp will not
run, instead you need to now run it as `lektor server -f gulp` which
will enable the gulp build.  gulp automatically builds your files
into `assets/static/dist`
 and this is where Lektor will then pick up the files.
  This is done so that you can ship the gulp generated assets
to others that do not have gulp installed which simplifies using a
Lektor website that uses gulp.

### Add support for browsersync in gulpfile.js for Time-saving

##### First install browser-sync

```bash
$ npm install --save-dev browser-sync
```

##### Add browserSync task in  gulpfile.js

```javascript
var browserSync = require('browser-sync') // [optional] makes your browser testing workflow faster by synchronising URLs

// Browser sync server for live reload
gulp.task('browserSync', function (done) {
  browserSync.init({
    proxy: 'localhost:5000',
    notify: false
  })
  done()
})

// [required] task name must be 'watch'
// `lektor server -f gulp` will execute this task
gulp.task('watch', gulp.parallel('browserSync', function () {
  gulp.watch(paths.styles.src, gulp.series('clean', gulp.parallel('styles', 'common'))).on('change', browserSync.reload)
  gulp.watch(paths.scripts.src, gulp.series('scripts')).on('change', browserSync.reload)
}))
```

## Manual Builds
> `lektor build -f gulp` will manually trigger a build and also invokes the gulp default task.

## Including The Files

Now you need to include the files in your template.  This will do it:

```html
<link rel="stylesheet" href="{{ '/static/dist/css/main.min.css'|asseturl }}">
<script type=text/javascript src="{{ '/static/dist/js/app.min.js'|asseturl }}" charset="utf-8"></script>
```

