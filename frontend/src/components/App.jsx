// @flow
import React, { type Node } from 'react';
import { Client as Styletron } from 'styletron-engine-atomic';
import { Provider as StyletronProvider } from 'styletron-react';
import { DarkTheme, ThemeProvider, styled } from 'baseui';
import { Block } from 'baseui/block';
import {
  HeaderNavigation,
  ALIGN,
  StyledNavigationItem as NavigationItem,
  StyledNavigationList as NavigationList,
} from 'baseui/header-navigation';
import ASLDetector from './ASLDetector2';

const engine = new Styletron();

const Centered = styled('div', {
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
  position: 'absolute',
  top: 0,
  bottom: 0,
  left: 0,
  right: 0,

  margin: 'auto',
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
      <HeaderNavigation>
        <NavigationList align={ALIGN.center}>
          <NavigationItem>ASL Detector</NavigationItem>
        </NavigationList>
      </HeaderNavigation>
      <Block overrides={BlockOverrides}>
        <Centered>
          <ASLDetector />
        </Centered>
      </Block>
    </ThemeProvider>
  </StyletronProvider>
);

export default App;
