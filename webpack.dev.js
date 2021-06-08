const { merge } = require("webpack-merge");
const common = require("./webpack.common.js");
const dev = {
    mode: "development",
    devtool: "source-map",
};

module.exports = merge(common, dev);
