const path = require("path");

module.exports = {
  entry: "./static_src/js/index.js",
  output: {
    filename: "[name].js",
    path: path.resolve(__dirname, "static/js"),
  },
  module: {
    rules: [
      {
        test: /\.js$/,
        exclude: /(node_modules)/,
        use: {
          loader: "babel-loader",
          options: {
            presets: ["@babel/preset-env"],
          },
        },
      },
    ],
  },
};
