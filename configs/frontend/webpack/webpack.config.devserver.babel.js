// @flow
import { HotModuleReplacementPlugin } from 'webpack';
import merge from 'webpack-merge';
import WriteFilePlugin from 'write-file-webpack-plugin';
import chalk from 'chalk';
import webpackDev from './webpack.config.dev.babel';
import outputDir from '../lib';

const port = process.env.PORT || 3000;

const frontendUrl = `http://localhost:${port}/`;

console.log(chalk.green(`The frontend will be run on ${frontendUrl}`));

export default function(env, argv) {
  const open = argv.auto ? JSON.parse(argv.auto) : true;

  return merge.smartStrategy({
    entry: 'prepend',
    plugins: 'append',
  })(webpackDev, {
    entry: [
      `webpack-dev-server/client?${frontendUrl}`,
      'webpack/hot/only-dev-server',
    ],

    devServer: {
      https: false,
      open,
      openPage: '',
      overlay: true,
      compress: true,
      stats: 'errors-only',
      publicPath: '/bundles',
      lazy: false,
      port,
      hot: true,
      historyApiFallback: false,
      inline: false,
      contentBase: outputDir,
      watchContentBase: true,
    },

    plugins: [
      new WriteFilePlugin({
        test: /\.((woff(2)?|ttf|eot|svg)(\?v=\d+\.\d+\.\d+)?)|(html|ejs)$/,
        useHashIndex: true,
      }),

      new HotModuleReplacementPlugin({}),
    ],
  });
}
