var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
	context: __dirname,
	entry: {
        schedule_change: './assets/js/schedule_change',
		appels: './assets/js/appels'
	},

	output: {
		path: path.resolve('./static/bundles/'),
		filename: "[name]-[hash].js"
	},

    plugins: [
		new BundleTracker({filename: './webpack-stats.json'}),
		new webpack.optimize.CommonsChunkPlugin({
			name: "commons",
			chunks: ["schedule_change", "appels"],
			minChunks: 2
		}),
	],

	resolve: {
		alias: {
			vue: 'vue/dist/vue.js'
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
			}
		]
	}
}
