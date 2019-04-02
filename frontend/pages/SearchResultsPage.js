'use strict';

import {
  StyleSheet,
  Image,
  View,
  TouchableHighlight,
  ActivityIndicator,
  FlatList,
} from 'react-native';
import React from 'react';
import { Text } from 'react-native-elements';
import { searchForItem } from '../utils/api';

class ListItem extends React.PureComponent {
    _onPress = () => {
      this.props.onPressItem(this.props.item);
    }

    render() {
      const name = this.props.item.name;
      const image = this.props.item.image_url;
      return (
        <TouchableHighlight
          style={this.props.style}
          onPress={this._onPress}
          underlayColor='#dddddd'>
          <View>
            <View style={styles.rowContainer}>
              <Image style={styles.thumb} source={{ uri: image }} />
              <View style={styles.textContainer}>
                <Text style={styles.title}
                  numberOfLines={1}>{name}</Text>
              </View>
            </View>
            <View style={styles.separator}/>
          </View>
        </TouchableHighlight>
      );
    }
}

export default class SearchResultsPage extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      searchResults: [],
      isLoading: true
    }
  }

    searchResults = async keyword => {
      const result = await searchForItem(keyword);
      this.setState({
        searchResults: result,
        isLoading: false
      })
    }

    componentDidMount(){
      const keyword = this.props.navigation.getParam("keyword", "");
      this.searchResults(keyword);
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
            <View style = {styles.ghostItemContainer}>
              <View style = {styles.separator}/>
              <ListItem
                item={{name: "+ Add Other Item"}}
                onPressItem={() => {this.props.navigation.navigate("AddItem")}}/>
            </View>
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
    separator: {
      height: 1,
      backgroundColor: '#dddddd'
    },
    title: {
      fontSize: 25,
      color: '#000000',
      marginTop: 20
    },
    rowContainer: {
      flexDirection: 'row',
      padding: 10
    },
    ghostItemContainer: {
      justifyContent: 'flex-end',
      backgroundColor: 'white',
      alignItems: 'center'
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
