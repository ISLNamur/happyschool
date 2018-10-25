var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
	context: __dirname,
	entry: {
		babelPolyfill: "babel-polyfill",
		menu: './assets/js/menu',
		annuaire: './assets/js/annuaire',
		appels: './assets/js/appels',
		mail_notification: './assets/js/mail_notification',
		mail_notification_list: './assets/js/mail_notification_list',
		members: './assets/js/members',
		mail_answer: './assets/js/mail_answer',
		answer: './assets/js/answer',
		dossier_eleve: './assets/js/dossier_eleve',
		ask_sanctions: './assets/js/ask_sanctions',
		infirmerie: './assets/js/infirmerie',
		schedule_change: './assets/js/schedule_change',
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
				"mail_notification_list", "members", "mail_answer", "dossier_eleve",
				"ask_sanctions", "annuaire", "infirmerie", "schedule_change",
			],
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
			},
			{
				test: /\.js$/,
				exclude: /node_modules/,
				use: 'babel-loader',
			}
		]
	}
}
