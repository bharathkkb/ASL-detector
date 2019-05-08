// @flow
import React, { Fragment, type Node } from 'react';
import { Card, StyledBody, StyledAction, StyledThumbnail } from 'baseui/card';
import { Button } from 'baseui/button';
import { H1 } from 'baseui/typography';

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
      <Card title="Result">
        <StyledBody>
          {'The prediction in ASL is "{prediction}".'}
          <H1 padding="0" margin="0" id="prediction">
            {prediction}
          </H1>
          <img src={src} alt={`${prediction} in ASL`} />
        </StyledBody>
      </Card>
      <br />
    </Fragment>
  );
};

export default Prediction;
