// @flow
import 'dotenv/config';
import { EnvironmentPlugin, ProvidePlugin } from 'webpack';
import HtmlWebpackPlugin from 'html-webpack-plugin';
import path from 'path';
import titleCase from 'title-case';
import Globals from './globals';
import { productName as name } from '../../../package.json';
const outputDir = path.join(__dirname, '../../../public');

const title = titleCase(name);

export default {
  target: 'web',

  context: path.join(__dirname, '..'),

  entry: [require.resolve('../../../assets/js/index.jsx')],

  resolve: {
    extensions: ['.js', '.jsx', '.json'],
  },

  output: {
    path: path.join(outputDir, './bundles/'),
    publicPath: './bundles/',
  },

  module: {
    rules: [
      {
        test: /\.css$/,
        use: [
          { loader: 'style-loader', options: { sourceMap: true } },
          { loader: 'css-loader' },
        ],
      },

      {
        test: /\.(png|jpg|gif)$/,
        use: [{ loader: 'url-loader' }],
      },
    ],
  },

  plugins: [
    new EnvironmentPlugin({
      DEBUG: JSON.stringify(process.env.DEBUG) || false,
      TITLE: title,
      REACT_ROOT: 'root',
    }),

    new ProvidePlugin(Globals),

    new HtmlWebpackPlugin({
      title,
      inject: true,
      template: require.resolve('../../../assets/templates/index.ejs'),
      filename: path.join(outputDir, './index.html'),
    }),
  ],
};
