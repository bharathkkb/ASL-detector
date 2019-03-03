'use strict';

module.exports = (api) => {
  console.log('foo');
  return {
    presets: [
      [require('./configs/frontend/webpack/babel-preset-local'), {node: true}],
    ],
  }
}