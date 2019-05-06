// @flow
import React, { Component, Fragment, type Node } from 'react';
import Webcam from 'react-webcam';
import {
  Modal,
  ModalHeader,
  ModalBody,
  ModalFooter,
  ModalButton,
} from 'baseui/modal';

type Props = {
  isOpen: boolean,
  onClose: () => any,
  onConfirm: (src: string) => any,
};

type State = {|
  screenshotUrl: ?string,
|};

export default class WebcamModal extends Component<Props, State> {
  props: Props;

  webcam: ?Webcam;

  state: State = {
    screenshotUrl: null,
  };

  handleClose = () => {
    this.setState({ screenshotUrl: null });
    this.props.onClose();
  };

  takeScreenshot = () => {
    if (!this.webcam) {
      return;
    }

    const screenshotUrl = this.webcam.getScreenshot();
    this.setState({ screenshotUrl });
  };

  handleConfirm = () => {
    const { screenshotUrl } = this.state;

    if (!screenshotUrl) {
      return;
    }

    this.setState({ screenshotUrl: null });
    this.props.onConfirm(screenshotUrl);
  };

  handleRetake = () => {
    this.setState({ screenshotUrl: null });
  };

  render(): Node {
    return (
      <Modal isOpen={this.props.isOpen} onClose={this.handleClose}>
        <ModalHeader>Webcam photo</ModalHeader>
        <ModalBody>
          {this.state.screenshotUrl ? (
            <img src={this.state.screenshotUrl} alt="Webcam Screenshot" />
          ) : (
            <Webcam
              audio={false}
              ref={webcam => {
                this.webcam = webcam;
              }}
              screenshotFormat="image/jpeg"
              width="100%"
            />
          )}
        </ModalBody>
        <ModalFooter>
          {this.state.screenshotUrl ? (
            <Fragment>
              <ModalButton onClick={this.handleConfirm}>Confirm</ModalButton>
              <ModalButton onClick={this.handleRetake}>Retake</ModalButton>
            </Fragment>
          ) : (
            <ModalButton onClick={this.takeScreenshot}>Take</ModalButton>
          )}
          <ModalButton onClick={this.handleClose}>Close</ModalButton>
        </ModalFooter>
      </Modal>
    );
  }
}
