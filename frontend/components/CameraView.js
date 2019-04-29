import React from 'react';
import {
  View, TouchableOpacity, ActivityIndicator, StyleSheet,
} from 'react-native';
import { Camera, Permissions } from 'expo';
import { Text, Button } from 'react-native-elements';
import { Ionicons } from '@expo/vector-icons';

const styles = StyleSheet.create({
  container: {
    flex: 1,
  },
  imageOverlay: {
    flex: 1,
    backgroundColor: 'transparent',
    flexDirection: 'row',
    justifyContent: 'center',
  },
  overlayButton: {
    flex: 1,
    alignSelf: 'flex-end',
  },
  alignCenter: {
    alignItems: 'center',
  },
});

export default class CameraView extends React.Component {
  state = {
    hasCameraPermission: null,
    type: Camera.Constants.Type.back,
  }

  async componentDidMount() {
    const { status } = await Permissions.askAsync(Permissions.CAMERA);
    this.setState({ hasCameraPermission: status === 'granted' });
  }

  handlePictureTaken = (image) => {
    // When the image data is returned to us
    // exit the camera view and pass the image back to the main view
    this.props.navigation.goBack();
    this.props.navigation.getParam('handlePictureTaken')(image);
  }

  /**
   * renders camera view
   *
   * @return rendered camera view
   */
  render() {
    const { hasCameraPermission } = this.state;
    // Check that permission was granted
    if (hasCameraPermission === null) {
      return <View />;
    } if (hasCameraPermission === false) {
      return <Text>No access to camera</Text>;
    }
    return (
    // main view holding the camera
      <View style={styles.container}>
        <Camera
          style={styles.container}
          type={this.state.type}
          ref={(ref) => { this.camera = ref; }}
        >
          {/* If the camera is taking a picture (loading) then overlay a spinner */}
          {this.state.loading ? (
            <View style={styles.imageOverlay}>
              <ActivityIndicator size="large" />
            </View>
          ) : (
          // If the camera is not taking a picture then show a view of buttons
            <View style={styles.imageOverlay}>
              {/* Flip button */}
              <TouchableOpacity
                style={[styles.overlayButton, styles.alignCenter]}
                onPress={() => {
                  this.setState(state => ({
                    type: state.type === Camera.Constants.Type.back
                      ? Camera.Constants.Type.front
                      : Camera.Constants.Type.back,
                  }));
                }}
              >
                <Text style={{ fontSize: 18, marginBottom: 10, color: 'white' }}>
                  {' '}
Flip
                  {' '}
                </Text>
              </TouchableOpacity>
              {/* Take a picture button */}
              <Button
                title="  Take Picture"
                raised
                icon={<Ionicons name="ios-camera" size={24} color="white" />}
                containerStyle={styles.overlayButton}
                onPress={() => {
                  this.setState({ loading: true });
                  this.camera.takePictureAsync({
                    quality: 0.5,
                    base64: true,
                    onPictureSaved: this.handlePictureTaken,
                  });
                }}
              />
              {/* Empty button to occupy left over space */}
              <View style={styles.overlayButton} />
            </View>
          )}
        </Camera>
      </View>
    );
  }
}
