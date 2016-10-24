"use strict";

var cosmiconfig = require('cosmiconfig'),
    explorer = cosmiconfig('.stylelintrc.json', options: [{
      rcExtension: true,
      cache: false
    }]);

explorer.load(null, 'stylelint.config.js')
  .then((result) => {
    // result.config is the parsed configuration object
    // result.filepath is the path to the config file that was found
  })
  .catch((parsingError) => {
    console.log('Stylelint cosmiconfig isn\'t set up correctly');
  });
