module.exports = (api, {node})=>{
  const devEnv = api.env('development');
  const testEnv = api.env('test');

  return {
    presets: [
      [require('@babel/preset-env'), {
        useBuiltIns: 'usage',
        ...(node ? {
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
    ].filter(Boolean),
  };
}