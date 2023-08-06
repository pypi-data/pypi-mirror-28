const LodashModuleReplacementPlugin = require("lodash-webpack-plugin");
const webpack = require("webpack");
const path = require("path");

module.exports = {
  entry: {
    app: "./index.js",
    vendor: [
      "react",
      "react-dom",
      "react-redux",
      "redux",
      "redux-observable",
      "immutable",
      "rxjs",
      "jquery"
    ]
  },
  target: "web",
  output: {
    path: path.join(__dirname, "lib"),
    filename: "main.js"
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /node_modules\/(?!(@nteract|rx-jupyter|rx-binder))/,
        loader: "babel-loader"
      },
      { test: /\.json$/, loader: "json-loader" }
    ]
  },
  resolve: {
    mainFields: ["nteractDesktop", "module", "main"],
    extensions: [".js", ".jsx"],
    alias: {
      "@nteract/core": "@nteract/core/src",
      "rx-jupyter": "rx-jupyter/src",
      "rx-binder": "rx-binder/src"
    }
  },
  plugins: [
    new LodashModuleReplacementPlugin(),
    new webpack.optimize.ModuleConcatenationPlugin(),

    // new webpack.IgnorePlugin(/\.(css|less)$/),

    // build vendor bundle (including common code chunks used in other bundles)
    new webpack.optimize.CommonsChunkPlugin({
      name: "vendor",
      filename: "vendor.js"
    }),
    new webpack.SourceMapDevToolPlugin({
      filename: "[name].js.map",
      exclude: ["vendor.js"]
    })
  ]
};
