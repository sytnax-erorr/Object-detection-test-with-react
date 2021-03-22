const path = require('path')
const fs = require('fs');

module.exports = {
  entry: {
    app: ['@babel/polyfill', './js/app.js']
  },
  output: {
    path: path.resolve(__dirname, 'js'),
    filename: 'app.min.js'
  },
  devServer: {
	https: true,
	host: '0.0.0.0', 
	port: 443,       
	https: {
           key: fs.readFileSync( process.cwd() + '/cret/private.key' ),
           cert: fs.readFileSync( process.cwd() + '/cret/certificate.pem' ),
           ca: fs.readFileSync( process.cwd() + '/cret/ca_bundle.crt' ) 
	},
	disableHostCheck: true
  },
  module: {
    rules: [
      {
        test: /\.js?$/,
        exclude: /node_modules/,
        loader: 'babel-loader',
        query: {
          presets: ['@babel/preset-env']
        }
      }
    ]
  }
}
