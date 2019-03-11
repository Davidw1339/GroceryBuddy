'use strict';

import {
  StyleSheet,
  Image,
  View,
  TouchableHighlight,
  FlatList,
} from 'react-native';
import React from 'react';
import { Text } from 'react-native-elements';

class ListItem extends React.PureComponent {
    _onPress = () => {
      this.props.onPressItem(this.props.index);
    }
  
    render() {
      const name = this.props.name;
      const image = this.props.image;
      console.log(this.props.name);
      return (
        <TouchableHighlight
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
      searchResults: [{name:"Red Delicious Apple", 
      image:"https://steemitimages.com/DQmZpRgMSms57P2WE5qFzvGh42CpK6J9hn5tQBXA4ZtMNvk/apple-fruit.jpg"}, {name:"Red Delicious Apple", 
      image:"https://steemitimages.com/DQmZpRgMSms57P2WE5qFzvGh42CpK6J9hn5tQBXA4ZtMNvk/apple-fruit.jpg"}]
    }
  }

    searchResults = async keyword => {
      const result = await searchForItem(keyword);
      this.setState({
        searchResults: result
      })
      console.log(result);
      this.props.navigation.navigate(
       'Results', {searchResults: result.searchResults}
      );
    }

    componentDidMount(){
      const keyword = this.props.navigation.getParam("keyword", "");
    }

    static navigationOptions = {
        title: 'Search Results Page',
    };

    _keyExtractor = (item, index) => index.toString();

    _renderItem = ({item}) => {
        return <ListItem
          name={item.name}
          image={item.image}
          onPressItem={this._onPressItem}
        />
    };
      
    _onPressItem = (index) => {
        console.log("Pressed row: "+index);
    };

    render() {
        const { params } = this.props.navigation.state;
        console.log(this.state.searchResults);
        return (
          <View style = {styles.resultsContainer}>
            <FlatList 
                data={this.state.searchResults}
                keyExtractor={this._keyExtractor}
                renderItem={this._renderItem}/>
            <View style = {[styles.ghostItemContainer, styles.separator]}>
              <ListItem
                name={"+ Add Other Item"}
                onPressItem={this._onPressItem}/>
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
      justifyContent: "flex-end"
    },
    resultsContainer: {
      flex: 1
    }
  });  
