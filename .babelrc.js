'use strict';

module.exports = (api) => {
  const testEnv = api.env('test');
  const devEnv = api.env(['test', 'development']);
  const targets = {};
  if (testEnv) {
    targets.node = 10;
  }

  return {
    presets: [
      [require('@babel/preset-env'), {
        useBuiltIns: 'usage',
        ...(testEnv? {
          targets: {
            node: 10
          }
        } : {
          modules: false,
        })
      }],
      [require('@babel/preset-react'), {development: devEnv}],
      require('@babel/preset-flow'),
    ],

    plugins: [
      testEnv
        ? require('babel-plugin-dynamic-import-node')
        : require('@babel/plugin-syntax-dynamic-import'),

        [require('@babel/plugin-proposal-class-properties'), { loose: true }],
        [
          require('@babel/plugin-transform-runtime'),
          { helpers: false, regenerator: true },
        ],
      devEnv ? require('react-hot-loader/babel') : null,
    ].filter(Boolean)
  }
}