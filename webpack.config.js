"use strict"

var path = require("path"),
    webpack = require('webpack'),
    ExtractTextPlugin = require('extract-text-webpack-plugin');

require('babel-core/register')({
  presets: ['es2015', 'react']
});
require.extensions['.css'] = () => {
  return;
};
require('./iogt/static/css/home.css');

module.exports = {
  entry: './iogt/static/css/index.js', //Entry point on IoGT app - should require other js modules and dependencies
  output: {
    filename: "[name]-[hash].js",
    path: path.resolve('./iogt/static/css/build/'),
  },
  module: {
    loaders: [
      {
        test: /\.css$/,
        loader: ExtractTextPlugin.extract({
          fallbackLoader: "style-loader",
          loader: "css-loader",
        }),
      }
    ]
  },
  plugins:[
    new ExtractTextPlugin({
      filename: './iogt/static/css/styles.css'}),
  ],
}





