var path = require("path"),
    webpack = require('webpack'),
    BundleTracker = require('webpack-bundle-tracker');


module.exports = {
  contect: __dirname,
  entry: './assets/js/index', //Entry point on IoGT app - should require other js modules and dependencies
  output: {
    path: path.resolve('assets/bundles/'),
    filename: "[name]-[hash].js" //Might need to include comma but last property
  },
  plugins:[
    new BundleTracker({
      filename: './webpack-stats.json'
    })
  ],
  module: {
    loaders: [{
      test: /\.jsx?$/,
      exclude: /node_modules/,
      loader: 'babel-loader'
    }]
  },
  resolve: {
    moduleDirectories: ['node_modules'],
    extensions: ['','.js','.jsx']
  }

}