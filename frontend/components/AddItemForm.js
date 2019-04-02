import React from 'react';
import { View, StyleSheet, ScrollView, KeyboardAvoidingView } from 'react-native';
import { Ionicons } from '@expo/vector-icons';
import { Input, Text, Button } from 'react-native-elements';
import { addGroceryItem } from '../utils/api';

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
    },
    {
        name: "store",
        label: "Store",
        placeholder: "County Market",
    },
    {
        name: "lat",
        label: "Latitude",
        keyboardType: 'numeric',
        placeholder: "40.113264",
    },
    {
        name: "long",
        label: "Longitude",
        keyboardType: 'numeric',
        placeholder: "-88.233905",
    }
]

export default class AddItemForm extends React.Component {
  constructor(props) {
    super(props);
    this.state = { 
      name: '',
      upc: '',
      price: '',
      store: '',
      user: 'admin',
      lat: '',
      long: ''
    }
  }

  retrieveUPC = (type, data) => {
    this.setState({
      upc: data 
    });
  }

  openScanner = () => {
    this.props.navigation.navigate('Scanner', {
      handleBarCodeScanned: this.retrieveUPC
    });
  }

  submitItemForm = () => {
    console.log(this.state);
    addGroceryItem(this.state);
  }

  render() {
    return (
      <ScrollView>
        <KeyboardAvoidingView behavior="position" enabled>
          <View style={styles.container}>
          <Text h4>Add A Grocery Item</Text>
          {INPUT_FIELDS.map((fieldProps) => {
            return <Input
                key={fieldProps.name}
                onChangeText={(textInput) => this.setState({ [fieldProps.name]: textInput })}
                value={this.state[fieldProps.name]}
                containerStyle={styles.input}
                {...fieldProps}
                />
          })}
          <Button
            title="  Scan UPC"
            raised
            icon={<Ionicons name="ios-camera" size={24} color={"white"}/>}
            onPress={this.openScanner}
            containerStyle={styles.input}
            />
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
  input: {
    marginBottom: 20
  }
});