import React from 'react';
import { View, StyleSheet, Alert, TouchableNativeFeedback } from 'react-native';
import ItemSearchBar from '../components/ItemSearchBar';
import { Text, ListItem, Button } from 'react-native-elements';
import { dummyItems, createListDummyItems } from '../utils/dummyData'


export default class SearchPage extends React.Component {

  static navigationOptions = ({ navigation }) => {
    return {
      title: navigation.getParam('name', 'Create Shopping List'),
    };
  };

  constructor(props) {
    super(props);
    this.state = {
      //itemList: [],
      //itemList: createListDummyItems,
      stores: {},
      selectedStore: '',
    }
  }

  componentDidMount() {

  }

  addItem = (item) => {
    console.log("ADDING ITEM")
    newStores = Object.assign({}, this.state.stores);

    // set universal parameters for item
    strippedItem = {
      name: item.name, 
      imageUrl: item.image_url,
      upc: item.upc,
      quantity: 1
    }

    for (let i = 0; i < item.stores.length; i++) {
      storeName = item.stores[i].name
      if (!(storeName in newStores)) {
        // create new store, save lat and long
        newStores[storeName] = {};
        newStores[storeName].items = []
        newStores[storeName].lat = item.stores[i].location.lat
        newStores[storeName].long = item.stores[i].location.long
      }
      // set store specific parameters
      currentPrice = item.stores[i].prices[0]
      strippedItem.price = currentPrice.price
      strippedItem.upvotes = currentPrice.upvotes
      strippedItem.downvotes = currentPrice.downvotes

      newStores[storeName].items.push(strippedItem)
    }

    this.setState({stores: newStores}, () => {this.recalculateTotals()})
  }

  calculateStoreTotal = (storeName) => {
    items = this.state.stores[storeName].items
    sum = 0
    for (let i = 0; i < items.length; i++) {
      sum += items[i].price
    }
    return sum
  }

  // choose cheapest store for a particular list and update total
  recalculateTotals = () => {
    cheapestTotal = Number.MAX_VALUE;
    cheapestStore = '';
    self = this;
    Object.keys(this.state.stores).forEach(function(store) {
      storeTotal = self.calculateStoreTotal(store)
      if (storeTotal < cheapestTotal) {
        cheapestTotal = storeTotal;
        cheapestStore = store;
      }
    }) 

    console.log('Got cheapest store: ' + cheapestStore)
    this.setState({
      selectedStore: cheapestStore,
    })
  }

  // pop up alert asking user if they want to delete an item
  deleteAlert = (i) => {
    Alert.alert(
      'Delete',
      'Remove \'' + this.state.stores[this.state.selectedStore].items[i].name + '\' from your shopping list?',
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
    newStores = Object.assign({}, this.state.stores);
    Object.keys(this.state.stores).forEach(function(store) {
      newStores[store].items.splice(i,1)
    }) 
    this.setState({
      stores: newStores
    })
    this.recalculateTotals()
  }

  submitSearch = async keyword => {
    this.props.navigation.navigate("SearchResults", {keyword: keyword, handleAddItem: this.addItem})
  }

  launchShopping = () => {
    console.log("TITLE: " + this.props.navigation.getParam('name'));
    this.props.navigation.navigate("Shopping", {
      list: {
        name: this.props.navigation.getParam("name"), 
        store: this.state.selectedStore,
        lat: this.state.stores[this.state.selectedStore].lat,
        long: this.state.stores[this.state.selectedStore].long,
        items: this.state.stores[this.state.selectedStore].items
      }
    })
  }

  render() {
    if (this.state.selectedStore === '') {
      return (
        <View style={styles.container}>
        <ItemSearchBar onSearch={this.submitSearch} />

        <View style={styles.footer}>
          <ListItem
            title={'Total (0) items'}
            rightTitle={'$0.00'}
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
            title="Finish Shopping List"
            iconRight
            onPress={() => {this.props.navigation.navigate("Shopping")}}
          />
        </View>

      </View>
      );
    }
    return (
      <View style={styles.container}>
        <ItemSearchBar onSearch={this.submitSearch} />

        <View>
          {this.state.stores[this.state.selectedStore].items.map((l, i) => (
            <ListItem
              key={i}
              Component={TouchableNativeFeedback}
              onLongPress={() => this.deleteAlert(i)}
              leftAvatar={{ title: l.name, source: { uri: l.imageUrl } }}
              title={l.name}
              rightTitle={'$' + this.state.stores[this.state.selectedStore].items[i].price}
              bottomDivider
            />
          ))}
        </View>

        <View style={styles.footer}>
          <ListItem
            title={'Total (' + this.state.stores[this.state.selectedStore].items.length + ' items)'}
            subtitle={this.state.selectedStore}
            rightTitle={'$' + this.calculateStoreTotal(this.state.selectedStore)}
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
            title="Finish Shopping List"
            iconRight
            onPress={this.launchShopping}
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
    padding: 10
  },
  footer: {
    flex: 1,
    justifyContent: 'flex-end',
  }
});