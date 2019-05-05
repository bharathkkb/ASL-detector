// @flow
import React, { Fragment, type Node } from 'react';
import { Card, StyledBody, StyledAction, StyledThumbnail } from 'baseui/card';
import { Button } from 'baseui/button';

type Props = {
  prediction: ?string,
  src: ?string,
};

const Prediction = ({ prediction, src }: Props): Node => {
  if (!prediction) {
    return null;
  }

  return (
    <Fragment>
      <Card title={prediction} id="prediction">
        <StyledBody>
          <img src={src} alt="Prediction" />
        </StyledBody>
      </Card>
      <br />
    </Fragment>
  );
};

export default Prediction;
