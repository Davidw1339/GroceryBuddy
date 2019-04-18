import React from 'react';
import { View, StyleSheet, ScrollView, KeyboardAvoidingView, Image, Picker, Alert } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Input, Text, Button } from 'react-native-elements';
import { addGroceryItem, getNearestStores } from '../utils/api';
import { Location, Permissions, ImageManipulator } from 'expo';

const INPUT_FIELDS = [
    {
        name: "name",
        label: "Name",
        placeholder: "Apples"
    },
    {
        name: "upc",
        label: "UPC",
        keyboardType: 'numeric',
        placeholder: "00000000"
    },
    {
        name: "price",
        label: "Price",
        keyboardType: 'numeric',
        placeholder: "3.42"
    }
]

export default class AddItemForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      name: '',
      upc: '',
      price: '',
      nearest_store: '-',
      stores: [],
      store: '',
      lat: '',
      long: '',
      user: 'admin',
      image: '',
      image_uri: ''
    }
  }

  componentDidMount = () => {
    this.getLocationAsync();
  }

  /**
   * resize image and set state so image data can be sent to backend
   * 
   * @param image
   */
  retrievePicture = (image) => {
    ImageManipulator.manipulateAsync(image.uri, [{resize: {width: 300}}], {base64: true})
    .then((image) => {
      const base64_datauri = 'data:image/jpg;base64,' + image.base64;
      this.setState({image_uri: base64_datauri, image: image.base64});
    })
  }

  /**
   * navigates to camera
   */
  openCamera = () => {
    this.props.navigation.navigate('Camera', {
      handlePictureTaken: this.retrievePicture
    })
  }

  /**
   * set state so upc data can be sent to backend
   */
  retrieveUPC = (type, data) => {
    this.setState({
      upc: data
    });
  }

  /**
   * navigates to scanner
   */
  openScanner = () => {
    this.props.navigation.navigate('Scanner', {
      handleBarCodeScanned: this.retrieveUPC
    });
  }

  /**
   * submits form
   */
  submitItemForm = () => {
    console.log(this.state);
    let response = addGroceryItem(this.state);
    response.then((result) => {
      if (result.success) {
        Alert.alert('Item Added!', result.error);
      } else {
        Alert.alert('Item Error', result.error);
      }
      console.log(result)
    });
  }

  getLocationAsync = async () => {
    let { status } = await Permissions.askAsync(Permissions.LOCATION);
    if (status !== 'granted') {
        console.log("Permission to access location was denied");
    }

    let location = await Location.getCurrentPositionAsync({});
    let latitude = location.coords.latitude;
    let longitude = location.coords.longitude;
    let stores = await getNearestStores(latitude, longitude, 10);
    this.setState({
        stores: stores,
        nearest_store: stores[0].name,
        store: stores[0].name,
        lat: stores[0].lat,
        long: stores[0].long
    });
  }

  /**
   * renders add item form with text/photo inputs and upc scanning
   * 
   * @return rendered add item form
   */
  render() {
    return (
      <ScrollView>
        <KeyboardAvoidingView behavior="position" enabled>
          <View style={styles.container}>
          <Text h4 style={styles.input}>Add A Grocery Item</Text>
          {this.state.image_uri !== "" && (<Image style={[styles.image, styles.input]} source={{uri: this.state.image_uri}}/>)}
          <Button
            title="Take A Picture"
            raised
            onPress={this.openCamera}
            />
          {INPUT_FIELDS.map((fieldProps) => {
            return <Input
                key={fieldProps.name}
                onChangeText={(textInput) => this.setState({ [fieldProps.name]: textInput })}
                value={this.state[fieldProps.name]}
                containerStyle={styles.input}
                {...fieldProps}
                />
          })}
          <Text style={styles.label}>Location</Text>
          <Picker
            selectedValue={this.state.nearest_store}
            onValueChange={(nearest_store, position) => {
              let store = stores[position];
              this.setState({ 
                nearest_store,
                lat: store.lat,
                long: store.long,
                store: store.name
              })
            }}
            style={{ width: 320 }}
            mode="dropdown">
            {this.state.stores.map((store_item) => {
              return <Picker.Item
                  key={store_item.name}
                  label={store_item.name + " " + Number.parseFloat(store_item.distance).toFixed(1) + " mi"}
                  value={store_item.name}
                  />
            })}
          </Picker>
          <View style={styles.buttonGroup}>
            <Button
              title="  Scan UPC"
              raised
              icon={<Ionicons name="ios-camera" size={24} color={"white"}/>}
              onPress={this.openScanner}
              containerStyle={styles.button}
              />
            <Button
              title="  Get Location"
              raised
              icon={<Ionicons name="md-locate" size={24} color={"white"}/>}
              onPress={this.getLocationAsync}
              containerStyle={styles.button}
            />
          </View>
          <Button
            title="Submit Item"
            raised
            onPress={this.submitItemForm}
            />
          </View>
        </KeyboardAvoidingView>
      </ScrollView>
    );
  }
}


const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    paddingTop: 20
  },
  buttonGroup: {
    flexDirection: 'row'
  },
  button: {
    margin: 20
  },
  label: {
    fontSize: 18
  },
  input: {
    marginBottom: 20
  },
  image: {
    width: 200,
    height: 200
  }
});
