'use strict';

import {
  StyleSheet,
  Image,
  View,
  TouchableHighlight,
  TouchableNativeFeedback,
  ActivityIndicator,
  FlatList,
} from 'react-native';
import React from 'react';
import { Text } from 'react-native-elements';
import { searchForItem, searchByUPC } from '../utils/api';
import { Platform } from 'react-native'

class ListItem extends React.PureComponent {
    _onPress = () => {
      this.props.onPressItem(this.props.item);
    }

    // returns string representing price range of item
    getPriceRange = () => {
      if(this.props.item.stores == null) {
        return '';
      }
      let minPrice = Number.MAX_VALUE;
      let maxPrice = 0;
      for (let i = 0; i < this.props.item.stores.length; i++) {
        let lastIndex = this.props.item.stores[i].prices.length - 1;
        const price = this.props.item.stores[i].prices[lastIndex].price;
        if (price < minPrice) {
          minPrice = price;
        }
        if (price > maxPrice) {
          maxPrice = price;
        }
      }
      if (maxPrice == minPrice) {
        return '$' + Number(minPrice).toFixed(2);
      } else {
        return '$' + Number(minPrice).toFixed(2) + ' - $' + Number(maxPrice).toFixed(2);
      }
    }

    render() {
      const name = this.props.item.name;
      const image = this.props.item.image_url;
      const priceRange = this.getPriceRange();

      let TouchablePlatformSpecific = Platform.OS === 'ios' ? 
        TouchableHighlight : 
        TouchableNativeFeedback;

        return (
          <TouchablePlatformSpecific
            style={this.props.style}
            onPress={this._onPress}
            underlayColor='#dddddd'>
            <View>
              <View style={styles.rowContainer}>
                <Image style={styles.thumb} source={{ uri: image }} />
                <View style={styles.textContainer}>
                  <Text style={styles.title}
                    numberOfLines={1}>{name}</Text>
                  <Text style={styles.subtitle}
                    numberOfLines={1}>{priceRange}</Text>
                </View>
              </View>
              <View style={styles.separator}/>
            </View>
          </TouchablePlatformSpecific>   
        )
     };
}

export default class SearchResultsPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      searchResults: [],
      isLoading: true
    }
  }

    searchResults = async (keyword, upc) => {
      let result;
      // if keyword doesn't exist then attempt to search by UPC
      if(!keyword) {
        result = await searchByUPC(upc);
      } else {
        result = await searchForItem(keyword);
      }
      this.setState({
        searchResults: result,
        isLoading: false
      })
    }

    componentDidMount(){
      const keyword = this.props.navigation.getParam("keyword", "");
      const upc = this.props.navigation.getParam("upc", "");
      this.searchResults(keyword, upc);
    }

    static navigationOptions = {
        title: 'Search Results Page',
    };

    _keyExtractor = (item, index) => index.toString();

    _renderItem = ({item}) => {
        return <ListItem
          item={item}
          onPressItem={this._onPressItem}
        />
    };

    _onPressItem = (item) => {
      this.props.navigation.getParam('handleAddItem', () => {console.log('NO ADD FUNCTION PROVIDED')})(item);
      this.props.navigation.goBack();
    };

    render() {
        if (this.state.isLoading) {
          return (
            <View style={styles.spinnerContainer}>
              <ActivityIndicator size="large"/>
            </View>
          )
        }
        return (
          <View style = {styles.resultsContainer}>
            {this.state.searchResults.length === 0 &&
              <View style = {styles.spinnerContainer}>
                <Text style = {styles.title}>No Results Found :(</Text>
              </View>
            }
            <FlatList
                data={this.state.searchResults}
                keyExtractor={this._keyExtractor}
                renderItem={this._renderItem}/>
            {/* Add other item button */}
            <TouchableHighlight 
              style = {styles.ghostItemContainer}
              onPress={() => {this.props.navigation.navigate("AddItem")}}
              underlayColor='#dddddd'>
              <View>
                <View style = {styles.separator}/>
                <View>
                  <View style={styles.rowContainer}>
                    <View style={[styles.textContainer, styles.addItemTextContainer]}>
                      <Text style={[styles.title, styles.addItemText]}>+ Add Other Item</Text>
                    </View>
                  </View>
                </View>
              </View>
            </TouchableHighlight>
          </View>
        );
    }
}

const styles = StyleSheet.create({
    thumb: {
      width: 80,
      height: 80,
      marginRight: 10
    },
    textContainer: {
      flex: 1
    },
    addItemTextContainer: {
      paddingBottom: 20
    },
    addItemText: {
      textAlign: 'center'
    },
    separator: {
      height: 1,
      backgroundColor: '#dddddd'
    },
    title: {
      fontSize: 18,
      color: '#000000',
      marginTop: 20
    },
    subtitle: {
      fontSize: 16,
      color: '#000000',
      marginTop: 5
    },
    rowContainer: {
      flexDirection: 'row',
      padding: 10
    },
    ghostItemContainer: {
      justifyContent: 'flex-end',
      backgroundColor: 'white',
    },
    resultsContainer: {
      flex: 1
    },
    spinnerContainer: {
      flex: 1,
      justifyContent: 'center',
      alignItems: 'center'
    }
  });
