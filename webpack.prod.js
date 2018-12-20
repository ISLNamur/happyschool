const merge = require('webpack-merge');
const MinifyPlugin = require("babel-minify-webpack-plugin");
const common = require('./webpack.common.js');
var webpack = require('webpack');

module.exports = merge(common, {
  mode: 'production',
  plugins: [
      new MinifyPlugin({}, {}),
      new webpack.DefinePlugin({
        'process.env': {
          NODE_ENV: '"production"'
        }
      })
  ]
});
