import React from 'react';
import { StyleSheet, View } from 'react-native';
import { SearchBar, Button } from 'react-native-elements';
import { Ionicons } from '@expo/vector-icons';

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    alignItems: 'center',
    borderBottomColor: 'lightgray',
    borderBottomWidth: 1,
  },
  input: {
    flex: 1,
  },
  scanbutton: {
    height: 35,
  },
});

export default class ItemSearchBar extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      search: '',
    };
  }

  /**
   * renders search bar
   *
   * @return rendered search bar
   */
  render() {
    return (
      <View style={styles.container}>
        <SearchBar
          platform="android"
          placeholder="Grocery Item Name Here"
          onChangeText={search => this.setState({ search })}
          value={this.state.search}
          onSubmitEditing={() => this.props.onSearch(this.state.search)}
          containerStyle={styles.input}
        />
        <Button
          raised
          icon={<Ionicons name="ios-camera" size={24} color="white" />}
          onPress={this.props.onPressCamera}
          containerStyle={styles.scanbutton}
        />
      </View>
    );
  }
}
