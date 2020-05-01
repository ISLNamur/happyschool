const merge = require('webpack-merge');
const common = require('./webpack.common.js');
var webpack = require('webpack');
const shell = require('child_process').execSync ; 

const src= `./*/assets/*`;
const dist= `./assets/.`;

shell(`mkdir -p ${dist}`);
shell(`cp -r ${src} ${dist}`);

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
