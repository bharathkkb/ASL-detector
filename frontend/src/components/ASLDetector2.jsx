// @flow
import React, { Component, Fragment, type Node } from 'react';
import { Button } from 'baseui/button';
import { FileUploader } from 'baseui/file-uploader';
import { Spinner } from 'baseui/spinner';
import { styled } from 'baseui';
import delay from 'delay';
import { dataURLToBlob } from 'blob-util';
import Prediction from './Prediction';
import CropModal from './CropModal';
import WebcamModal from './WebcamModal';
import { predict, getPrediction } from '../helpers/apis';
import { getAlphabet } from '../helpers/alphabet';

const delayTime = 1000 * 1; // 1 second
const wait = () => delay(delayTime);

const Centered = styled('div', {
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
});

type Props = {};

type State = {|
  disabled: boolean,
  errorMessage: string,
  prediction: ?string,
  src: ?string,
  showWebcam: boolean,
  showCrop: boolean,
  uploadSrc: ?string,
|};

const resetState = Object.freeze({
  disabled: false,
  errorMessage: '',
  uploadSrc: null,
});

let prevId: ?string = null;

export default class ASLDetector2 extends Component<Props, State> {
  props: Props;

  state: State = {
    ...resetState,
    prediction: null,
    src: null,
    showWebcam: false,
    showCrop: false,
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
    this.setState({
      errorMessage: '',
      uploadSrc: URL.createObjectURL(file),
      showCrop: true,
    });
  };

  sendFile = async (file: Blob) => {
    this.setState({ disabled: true });
    console.log(file);
    const formData = new FormData();
    formData.append('file_to_upload', new File([file], 'image.jpeg'));
    let id;

    try {
      id = await predict(formData);
    } catch (err) {
      this.setState({ errorMessage: 'Problems connecting to server.' });
      return;
    }

    await this.waitforPrediction(id, file);
  };

  waitforPrediction = async (id: string, file: Blob) => {
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
    this.setState({
      errorMessage: '',
      showWebcam: false,
      uploadSrc: imgSrc,
      showCrop: true,
    });
    // console.log(imgSrc);
    // await this.sendFile(dataURLToBlob(imgSrc));
  };

  closeCrop = () => {
    this.setState({ showCrop: false });
  };

  confirmCrop = async (file: Blob) => {
    this.setState({ showCrop: false });
    await this.sendFile(file);
  };

  render(): Node {
    return (
      <div>
        {this.state.disabled ? (
          <Fragment>
            <Centered>
              <div>
                <Centered>
                  <Spinner />
                </Centered>
                <br />
                <Centered>
                  <Button onClick={this.handleCancel}>Cancel</Button>
                </Centered>
              </div>
            </Centered>
            <br />
          </Fragment>
        ) : null}
        <Prediction prediction={this.state.prediction} src={this.state.src} />
        <div id="imageupload">
          <FileUploader
            disabled={this.state.disabled}
            onDrop={this.handleDrop}
            onCancel={this.handleCancel}
            errorMessage={this.state.errorMessage}
            onRetry={this.reset}
          />
        </div>
        <br />
        <CropModal
          isOpen={this.state.showCrop}
          onClose={this.closeCrop}
          onConfirm={this.confirmCrop}
          src={this.state.uploadSrc}
        />
        <WebcamModal
          isOpen={this.state.showWebcam}
          onClose={this.closeWebcam}
          onConfirm={this.handleWebcamScreenshot}
        />
        <Centered>
          <Button onClick={this.openWebcam} disabled={this.state.disabled}>
            Use Webcam
          </Button>
        </Centered>
      </div>
    );
  }
}
