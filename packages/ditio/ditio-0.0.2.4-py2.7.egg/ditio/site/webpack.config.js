var path = require('path');
var src = path.resolve(__dirname, "./src")
var dist = path.resolve(__dirname,"./dist")
var static = path.resolve(__dirname,"./static")
console.log(src)
resolve = path.resolve;

module.exports = {
    entry: resolve(__dirname,"./src/index.jsx"),
    output:{
        path: __dirname, 
        //path: resolve(__dirname,"./dist"), 
        filename: "bundle.js"
    },
    module:{
        loaders:[
            { test: /\.css/, loader:"style-loader!css-loader" },
            { test: /\.js$/, loader: 'babel-loader', exclude: /node_modules/ ,include:  src },
            { test: /\.jsx$/, loader: 'babel-loader', exclude: /node_modules/ ,include:  src }
        ]
    }
}
