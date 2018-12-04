var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');
const fs = require('fs');

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
		path: path.resolve('./static/bundles/'),
		filename: "[name]-[hash].js"
	},

    plugins: [
		new BundleTracker({filename: './webpack-stats.json'}),
		new webpack.optimize.CommonsChunkPlugin({
			name: "commons",
			chunks: ["menu", "annuaire", "schedule_change", "appels", "mail_notification",
				"mail_notification_list", "members", "mail_answer", "dossier_eleve",
				"ask_sanctions", "infirmerie", "schedule_change",
				"admin",
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
