var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
const fs = require('fs');
const VueLoaderPlugin = require('vue-loader/lib/plugin')
const swCachePlugin = require('sw-cache-plugin');
const CopyPlugin = require('copy-webpack-plugin');

function getEntries () {
    let apps = fs.readdirSync('./assets/js/')
        .filter(
            (file) => file.match(/.*\.js$/)
        )
        .map((file) => {
            return {
                name: file.substring(0, file.length - 3),
                path: './assets/js/' + file
            }
        }).reduce((memo, file) => {
            memo[file.name] = [file.path]
            return memo;
		}, {})
	apps['polyfill'] = "@babel/polyfill";
	return apps;
}

module.exports = {
	context: __dirname,
	entry: getEntries(),
	output: {
		publicPath: '/static/bundles/',
		path: path.resolve('./static/bundles/'),
		filename: "[name]-[hash].js"
	},

    plugins: [
		new VueLoaderPlugin(),
		new BundleTracker({filename: './webpack-stats.json'}),
		new CopyPlugin([
			{
				from: '**', to: '', context: 'assets/sw/'
			},
			{
				from: 'with-async-ittr-min.js', to: 'idb.js', context: 'node_modules/idb/build/iife/'
			},
		], { logLevel: 'debug' }),
		new swCachePlugin(
			{
			  cacheName:'cacheName',
			  ignore: [/.*\.map$/],
			}
		  )
	],
	optimization: {
		namedModules: true, // NamedModulesPlugin()
		splitChunks: { // CommonsChunkPlugin()
			name: 'commons',
			chunks: 'all',
			minChunks: 2
		},
		noEmitOnErrors: true, // NoEmitOnErrorsPlugin
		concatenateModules: true //ModuleConcatenationPlugin
	},

	resolve: {
		alias: {
			vue: 'vue/dist/vue.common.js'
		}
	},

	module: {
		rules: [
			{
				test: /\.vue$/,
				loader: 'vue-loader',
				options: {
					loaders: {
					}
					// other vue-loader options go here
				}
			},
			{
				test: /\.css$/,
				use: [
					{ loader: "style-loader" },
					{ loader: "css-loader" }
				]
			},
			{
				test: /\.js$/,
				exclude: /node_modules/,
				use: 'babel-loader',
			}
		]
	}
}
