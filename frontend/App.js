import React from 'react';
import { ActivityIndicator, Text, TextInput, Button, View, StyleSheet } from 'react-native';
import fetch from 'node-fetch'

export default class App extends React.Component {
  constructor(props) {
    super(props);
    this.state = { isLoading: true }
  }

  refreshPrice = () => {
    ROUTE_URL = 'http://grocerybuddybackend.azurewebsites.net/testdb'
    BODY_KEY = '_bodyText'
    return fetch(ROUTE_URL)
      .then((response) => {
        this.setState({
          isLoading: false,
          dynamicText: response[BODY_KEY]
        })
      })
      .catch((error) => {
        console.error(error);
      });
  }

  componentDidMount() {
    this.refreshPrice();
  }

  // Takes the current value of the input field and submits it to the database
  submitPrice = () => {
    ROUTE_URL = 'http://grocerybuddybackend.azurewebsites.net/testdb?name=' + this.state.textInput
    return fetch(ROUTE_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      }
    })
    .then(response => {
      this.setState({
        textInput: ''
      });
      this.refreshPrice();
    })
    .catch((error) => {
      console.error(error);
    })
  }

  render() {
    if (this.state.isLoading) {
      return (
        <View style={styles.container}>
          <ActivityIndicator />
        </View>
      )
    }

    return (
      <View style={styles.container}>
        <Text>Price of apples: {this.state.dynamicText}</Text>
        <TextInput style={styles.input} onChangeText={(textInput) => this.setState({textInput})} value={this.state.textInput}/>
        <Button onPress={this.submitPrice} title="Submit Price"/>
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    alignItems: 'center',
    justifyContent: 'center',
  },
  input: {
    height: 40,
    width: 200,
    borderColor: 'gray',
    borderWidth: 1,
    borderRadius: 5,
    marginBottom: 10,
    padding: 5
  }
});