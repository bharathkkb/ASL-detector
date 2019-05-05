// @flow
import React, { Component, type Node } from 'react';
import { Button } from 'baseui/button';
import { FileUploader } from 'baseui/file-uploader';
import { Spinner } from 'baseui/spinner';
import delay from 'delay';
import { dataURLToBlob } from 'blob-util';
import Prediction from './Prediction';
import WebcamModal from './WebcamModal';
import { predict, getPrediction } from '../helpers/apis';
import { getAlphabet } from '../helpers/alphabet';

const delayTime = 1000 * 1; // 1 second
const wait = () => delay(delayTime);

type Props = {};

type State = {|
  disabled: boolean,
  errorMessage: string,
  prediction: ?string,
  src: ?string,
  showWebcam?: boolean,
|};

const resetState = Object.freeze({
  disabled: false,
  errorMessage: '',
});

let prevId: ?string = null;

export default class ASLDetector2 extends Component<Props, State> {
  props: Props;

  state: State = {
    ...resetState,
    prediction: null,
    src: null,
  };

  handleDrop = async (
    acceptedFiles: Array<File>,
    rejectedFiles: Array<File>
  ) => {
    if (acceptedFiles.length > 1) {
      this.setState({ errorMessage: 'You may only upload 1 file at a time.' });
      return;
    }

    if (rejectedFiles.length > 0) {
      this.setState({ errorMessage: 'Some files were rejected.' });
      return;
    }

    if (acceptedFiles.length === 0) {
      this.setState({ errorMessage: 'No files were accepted' });
      return;
    }

    const [file: File] = acceptedFiles;
    await this.sendFile(file);
  };

  sendFile = async (file: File) => {
    this.setState({ disabled: true });
    console.log(file);
    const formData = new FormData();
    formData.append('file_to_upload', file);
    let id;

    try {
      id = await predict(formData);
    } catch (err) {
      this.setState({ errorMessage: 'Problems connecting to server.' });
      return;
    }

    await this.waitforPrediction(id, file);
  };

  waitforPrediction = async (id: string, file: File) => {
    prevId = id;
    const idForm = new FormData();
    idForm.append('id', id);
    let data;

    let found = false;
    let predictionData;
    while (!found && prevId === id) {
      await wait();
      console.log('waiting...');
      try {
        data = await getPrediction(idForm);
      } catch (err) {
        this.reset();
        return;
      }

      if (data.result === 'complete') {
        found = true;
        predictionData = data.prediction;
      }
    }

    if (prevId !== id) {
      return;
    }

    const result = getAlphabet(predictionData);
    console.log(result);

    this.setState({
      prediction: result,
      src: URL.createObjectURL(file),
      disabled: false,
    });
  };

  reset = () => {
    this.setState({ ...resetState });
  };

  handleCancel = () => {
    this.reset();
    prevId = null;
  };

  openWebcam = () => {
    this.setState({ showWebcam: true });
  };

  closeWebcam = () => {
    this.setState({ showWebcam: false });
  };

  handleWebcamScreenshot = async (imgSrc: string) => {
    this.setState({ showWebcam: false });
    console.log(imgSrc);
    await this.sendFile(dataURLToBlob(imgSrc));
  };

  render(): Node {
    return (
      <div>
        {this.state.disabled ? (
          <>
            <Spinner />
            <Button onClick={this.handleCancel}>Cancel</Button>
          </>
        ) : null}
        <Prediction prediction={this.state.prediction} src={this.state.src} />
        <FileUploader
          disabled={this.state.disabled}
          onDrop={this.handleDrop}
          onCancel={this.handleCancel}
          errorMessage={this.state.errorMessage}
          onRetry={this.reset}
        />
        <WebcamModal
          isOpen={this.state.showWebcam}
          onClose={this.closeWebcam}
          onConfirm={this.handleWebcamScreenshot}
        />
        <Button onClick={this.openWebcam} disabled={this.state.disabled}>
          Use Webcam
        </Button>
      </div>
    );
  }
}
