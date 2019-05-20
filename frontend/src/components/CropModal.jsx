// @flow
import React, { Component, type Node } from 'react';
import {
  Modal,
  ModalHeader,
  ModalBody,
  ModalFooter,
  ModalButton,
} from 'baseui/modal';
import { styled } from 'baseui';
import ReactCrop from 'react-image-crop';
import { dataURLToBlob } from 'blob-util';
import 'react-image-crop/dist/ReactCrop.css';
import { string } from 'postcss-selector-parser';

const CROP_WIDTH = 200;

const CROP_HEIGHT = 200;

const Centered = styled('div', {
  display: 'flex',
  justifyContent: 'center',
  alignItems: 'center',
});

type Crop = {
  aspect?: number,
  x: number,
  y: number,
  width: number,
  height: number,
};

type Props = {
  isOpen: boolean,
  onClose: () => any,
  onConfirm: (file: Blob) => any,
  src: ?string,
};

type State = {|
  crop: Crop,
|};

const defaultCrop: Crop = {
  aspect: 1 / 1,
  x: 0,
  y: 0,
  width: CROP_WIDTH,
  height: CROP_HEIGHT,
};

const getCroppedImg = (
  image: HTMLImageElement,
  crop: Crop,
  fileName: string
): string => {
  const canvas = document.createElement('canvas');
  const scaleX = image.naturalWidth / image.width;
  const scaleY = image.naturalHeight / image.height;
  canvas.width = CROP_WIDTH;
  canvas.height = CROP_HEIGHT;
  const ctx = canvas.getContext('2d');

  ctx.drawImage(
    image,
    crop.x * scaleX,
    crop.y * scaleY,
    crop.width * scaleX,
    crop.height * scaleY,
    0,
    0,
    CROP_WIDTH,
    CROP_HEIGHT
  );

  const base64Image = canvas.toDataURL('image/jpeg');

  return base64Image;
};

export default class CropModal extends Component<Props, State> {
  props: Props;

  state: State = {
    crop: {
      ...defaultCrop,
    },
  };

  cropRef: ?ReactCrop;

  imageRef: ?HTMLImageElement;

  onCropChange = (crop: Crop) => {
    this.setState({ crop });
  };

  onImageLoaded = (image: HTMLImageElement) => {
    this.imageRef = image;
  };

  handleConfirm = async () => {
    if (!this.cropRef || !this.imageRef) {
      return;
    }

    const crop = this.cropRef.makeNewCrop();
    const croppedImageUrl = getCroppedImg(
      // $FlowFixMe
      this.imageRef,
      crop,
      'image.jpeg'
    );
    this.props.onConfirm(await dataURLToBlob(croppedImageUrl));
  };

  componentDidUpdate(prevProps: Props) {
    if (this.props.src !== prevProps.src) {
      // eslint-disable-next-line
      this.setState({ crop: { ...defaultCrop } });
    }
  }

  render() {
    return (
      <Modal isOpen={this.props.isOpen} onClose={this.props.onClose}>
        <ModalHeader>Crop Image</ModalHeader>
        <ModalBody>
          <Centered>
            {this.props.src ? (
              <ReactCrop
                src={this.props.src}
                crop={this.state.crop}
                onImageLoaded={this.onImageLoaded}
                onChange={this.onCropChange}
                ref={cropRef => {
                  this.cropRef = cropRef;
                }}
              />
            ) : null}
          </Centered>
        </ModalBody>
        <ModalFooter>
          <ModalButton id="crop-confirm" onClick={this.handleConfirm}>
            Confirm
          </ModalButton>
          <ModalButton onClick={this.props.onClose}>Close</ModalButton>
        </ModalFooter>
      </Modal>
    );
  }
}
