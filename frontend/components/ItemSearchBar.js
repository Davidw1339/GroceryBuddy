import React from 'react';
import { StyleSheet, Text, View } from 'react-native';
import { SearchBar } from 'react-native-elements';

export default class ItemSearchBar extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
        search: ''
    }
  }

  render() {
    return (
        <SearchBar
            platform="android"
            placeholder="Grocery Item Name Here"
            onChangeText={(search) => this.setState({search})}
            value={this.state.search}
            onSubmitEditing={() => this.props.onSearch(this.state.search)}
            containerStyle={styles.input}/>
    );
  }
}

const styles = StyleSheet.create({
  input: {
    width: '100%',
    borderBottomColor: "lightgray",
    borderBottomWidth: 1
  }
});