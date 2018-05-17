var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
	context: __dirname,
	entry: {
		menu: './assets/js/menu',
        schedule_change: './assets/js/schedule_change',
		appels: './assets/js/appels',
		mail_notification: './assets/js/mail_notification',
		mail_notification_list: './assets/js/mail_notification_list',
		members: './assets/js/members',
		mail_answer: './assets/js/mail_answer',
		answer: './assets/js/answer',
	},

	output: {
		path: path.resolve('./static/bundles/'),
		filename: "[name]-[hash].js"
	},

    plugins: [
		new BundleTracker({filename: './webpack-stats.json'}),
		new webpack.optimize.CommonsChunkPlugin({
			name: "commons",
			chunks: ["menu", "schedule_change", "appels", "mail_notification",
				"mail_notification_list", "members", "mail_answer", "answer"],
			minChunks: 2
		}),
	],

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
			}
		]
	}
}
