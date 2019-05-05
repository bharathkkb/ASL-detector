// @flow
import React, { type Node } from 'react';
import { Client as Styletron } from 'styletron-engine-atomic';
import { Provider as StyletronProvider } from 'styletron-react';
import { DarkTheme, ThemeProvider, styled } from 'baseui';
import { Block } from 'baseui/block';
import ASLDetector from './ASLDetector2';

const engine = new Styletron();

const Centered = styled('div', {
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
});

const BlockOverrides = {
  Block: {
    style: ({ $theme }) => ({
      backgroundColor: $theme.colors.background,
      maxWidth: '100vw',
      overflow: 'hidden',
      minHeight: '100vh',
    }),
  },
};

const App = (): Node => (
  <StyletronProvider value={engine}>
    <ThemeProvider theme={DarkTheme}>
      <Block overrides={BlockOverrides}>
        <Centered>
          <ASLDetector />
        </Centered>
      </Block>
    </ThemeProvider>
  </StyletronProvider>
);

export default App;
