const merge = require('webpack-merge');
const common = require('./webpack.common.js');
var webpack = require('webpack');
const shell = require('child_process').execSync ; 

const src= `./*/assets/*`;
const dist= `./assets/.`;

shell(`mkdir -p ${dist}`);
shell(`if ls ./*/assets/* 1> /dev/null 2>&1; then cp -r ${src} ${dist}; fi`, {shell: '/bin/bash'});

module.exports = merge(common, {
  mode: 'production',
  plugins: [
      new webpack.DefinePlugin({
        'process.env': {
          NODE_ENV: '"production"'
        }
      })
  ]
});
