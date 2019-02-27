import React from 'react';
import { View, StyleSheet } from 'react-native';
import ItemSearchBar from '../components/ItemSearchBar';
import { Text } from 'react-native-elements';
import { searchForItem } from '../utils/api';

export default class SearchPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      searchResults: []
    }
  }

  submitSearch = async keyword => {
    const result = await searchForItem(keyword);
    this.setState({
      searchResults: result
    })
    console.log(result);
  }

  render() {
    return (
      <View style={styles.container}>
        <ItemSearchBar onSearch={this.submitSearch}/>
        {this.state.searchResults.map((searchResult, i) => {
          console.log(searchResult);
          return (
            <View key={i}>
              <Text h4 key={i}>{searchResult.name}</Text>
              <Text key={searchResult.upc + i}>UPC: {searchResult.upc} Price: {searchResult.stores[0].price[0].price}</Text>
            </View>
          )
        })}
      </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    paddingTop: 30,
    padding: 10
  }
});