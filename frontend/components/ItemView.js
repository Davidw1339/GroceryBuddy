'use strict';

import React, { Component } from 'react'
import {
  StyleSheet,
  View,
  Text
} from 'react-native';

export default class ItemView extends React.Component {
  static navigationOptions = {
    title: 'Item Details',
  };

  /**
   * renders item with price
   * 
   * @return rendered item
   */
  render() {
    const { params } = this.props.navigation.state;
    let item = params.item;
    let name = item.name;
    let price = '$' + item.price;

    return (
        <View style={styles.heading}>
          <Text style={styles.name}>{name}</Text>
          <Text style={styles.price}>{price}</Text>
        </View>
    );
  }
}

const styles = StyleSheet.create({
  container: {
    marginTop: 65
  },
  heading: {
    backgroundColor: '#F8F8F8',
  },
  name: {
    fontSize: 25,
    fontWeight: 'bold',
    margin: 5,
    color: '#656565'
  },
  price: {
    fontSize: 20,
    fontWeight: 'bold',
    margin: 5,
    color: '#48BBEC'
  },
  title: {
    fontSize: 20,
    margin: 5,
    color: '#656565'
  },
});