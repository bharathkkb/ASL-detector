// @flow
import React, { Component, type Node } from 'react';
import delay from 'delay';
import { predict, getPrediction } from '../helpers/apis';
import { getAlphabet } from '../helpers/alphabet';

const delayTime = 1000 * 1; // 1 second

const wait = () => delay(delayTime);

type Props = {};

type State = {
  isLoading: boolean,
  prediction: ?string,
};

const Loading = ({
  isLoading,
  children,
}: {
  isLoading: boolean,
  children: Node,
}): Node => {
  if (isLoading) {
    return null;
  }
  return children;
};

const Prediction = ({ prediction }: { prediction: ?string }): Node => {
  if (!prediction) {
    return null;
  }
  return (
    <div style={{ textAlign: 'center' }} id="prediction">
      {prediction}
    </div>
  );
};

export default class App extends Component<Props, State> {
  props: Props;

  state: State = {
    isLoading: false,
    prediction: null,
  };

  submit = async (event: SyntheticEvent<HTMLInputElement>) => {
    const [file: File] = event.currentTarget.files;
    const formData = new FormData();
    formData.append('file_to_upload', file);
    let id;

    try {
      id = await predict(formData);
    } catch (err) {
      return;
    }

    this.setState({ isLoading: true });

    const idForm = new FormData();
    idForm.append('id', id);
    let data;

    let found = false;
    let predictionData;
    while (!found) {
      await wait();
      try {
        data = await getPrediction(idForm);
      } catch (err) {
        this.setState({ isLoading: false });
        return;
      }

      if (data.result === 'complete') {
        found = true;
        predictionData = data.prediction;
      }
    }

    this.setState({
      isLoading: false,
      prediction: getAlphabet(predictionData),
    });
  };

  render() {
    return (
      <div>
        <Prediction prediction={this.state.prediction} />
        <Loading isLoading={this.state.isLoading}>
          <input type="file" onChange={this.submit} id="imageupload" />
        </Loading>
      </div>
    );
  }
}
