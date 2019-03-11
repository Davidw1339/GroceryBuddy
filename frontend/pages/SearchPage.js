import React from 'react';
import { View, StyleSheet, FlatList, ScrollView, Alert, TouchableNativeFeedback, Picker } from 'react-native';
import ItemSearchBar from '../components/ItemSearchBar';
import { Text, ListItem, Button } from 'react-native-elements';
import { searchForItem } from '../utils/api';
import { dummyItems, createListDummyItems } from '../utils/dummyData'


export default class SearchPage extends React.Component {

  static navigationOptions = {
    title: 'Create Shopping List',
  };

  constructor(props) {
    super(props);
    this.state = {
      searchResults: [],
      //itemList: []
      itemList: createListDummyItems,
      selectedStore: '',
      currentTotal: 0
    }
  }

  componentDidMount() {
    this.selectCheapestStore()
  }

  submitSearch = async keyword => {
    const result = await searchForItem(keyword);
    this.setState({
      searchResults: result
    })
    console.log(result);
  }

  // pop up alert asking user if they want to delete an item
  deleteAlert = (i) => {
    Alert.alert(
      'Delete',
      'Remove \'' + this.state.itemList[i].name + '\' from your shopping list?',
      [
        {text: 'Cancel', style: 'cancel'},
        {
          text: 'OK', 
          onPress: () => this.deleteItem(i)
        },
      ],
      {cancelable: true},
    );
  }

  // delete item with index i from shopping list
  deleteItem = (i) => {
    // copy list
    newList = [...this.state.itemList];
    newList.splice(i, 1);
    this.setState({
      itemList: newList
    })
    this.selectCheapestStore()
  }

  // choose cheapest store out of the items
  selectCheapestStore = () => {
    // uses store name as key
    storeTotals = {}
    for (let i = 0; i < this.state.itemList.length; i++) {
      stores = this.state.itemList[i].stores;
      for (let j = 0; j < stores.length; j++) {
        if (!(stores[j].name in storeTotals)) {
          storeTotals[stores[j].name] = 0;
        }
        storeTotals[stores[j].name] += this.getItemPrice(i, stores[j].name)
      }
    }
    cheapestTotal = Number.MAX_VALUE;
    cheapestStore = '';
    Object.keys(storeTotals).forEach(function(key) {
      if (storeTotals[key] < cheapestTotal) {
        cheapestTotal = storeTotals[key];
        cheapestStore = key;
      }
    }) 
    if (cheapestStore == '') {
      cheapestTotal = 0;
    }

    this.setState({
      selectedStore: cheapestStore,
      currentTotal: cheapestTotal
    })

  }

  // calculate item with index i price for a certain store
  getItemPrice = (i, store) => {
    stores = this.state.itemList[i].stores
    for (let i = 0; i < stores.length; i++) {
      // this may need to check lat and long
      if (stores[i].name == store) {
        console.log(stores[i].prices[0].price)
        return stores[i].prices[0].price;
      }
    } 
    return -1
  }

  

  render() {
    return (
      <View style={styles.container}>
        <ItemSearchBar onSearch={this.submitSearch} />
        {this.state.searchResults.map((searchResult, i) => {
          console.log(searchResult);
          return (
            <View key={i}>
              <Text h4 key={i}>{searchResult.name}</Text>
              <Text key={searchResult.upc + i}>UPC: {searchResult.upc} Price: {searchResult.stores[0].price[0].price}</Text>
            </View>
          )
        })}

        <View>
          {this.state.itemList.map((l, i) => (
            <ListItem
              key={i}
              Component={TouchableNativeFeedback}
              onLongPress={() => this.deleteAlert(i)}
              leftAvatar={{ title: l.name[0], source: { uri: l.image_url } }}
              title={l.name}
              rightTitle={'$' + this.getItemPrice(i, this.state.selectedStore)}
              bottomDivider
            />
          ))}
        </View>

        <View style={styles.footer}>
          <ListItem
            title={'Total (' + this.state.itemList.length + ' items)'}
            subtitle={this.state.selectedStore}
            rightTitle={'$' + this.state.currentTotal}
            topDivider
          />
        </View>
        <View>
          <Button
            icon={{
              name: "check",
              size: 20,
              color: "white"
            }}
            title="Finish List"
            iconRight
            onPress={() => {this.props.navigation.navigate("Shopping")}}
          />
        </View>

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
  },
  footer: {
    flex: 1,
    justifyContent: 'flex-end',
  }
});