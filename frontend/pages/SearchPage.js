import React from 'react';

import { View, StyleSheet, Alert, TouchableNativeFeedback, TouchableHighlight, FlatList, Card, Platform } from 'react-native';
import ItemSearchBar from '../components/ItemSearchBar';
import { Text, ListItem, Button, Avatar, Icon, Badge } from 'react-native-elements';
import Collapsible from 'react-native-collapsible';

export default class SearchPage extends React.Component {

  static navigationOptions = ({ navigation }) => {
    return {
      title: navigation.getParam('name', 'Create Shopping List'),
    };
  };

  constructor(props) {
    super(props);
    this.state = {
      stores: {},
      selectedStore: '',
      isCollapsed: true
    }
  }

  addItem = (item) => {
    console.log("ADDING ITEM")
    console.log(item)
    newStores = Object.assign({}, this.state.stores);

    cheapestPrice = Number.MAX_VALUE;
    cheapestItem = null;

    for (let i = 0; i < item.stores.length; i++) {
      storeName = item.stores[i].name
      if (!(storeName in newStores)) {
        // create new store, save lat and long
        newStores[storeName] = {};
        newStores[storeName].items = []
        newStores[storeName].lat = item.stores[i].location.lat
        newStores[storeName].long = item.stores[i].location.long
      }

      // set universal parameters for item
      strippedItem = {
        name: item.name,
        imageUrl: item.image_url,
        upc: item.upc,
        quantity: 1,
        cheapest: false
      }
      
      // set store specific parameters
      let lastIndex = item.stores[i].prices.length - 1
      currentPrice = item.stores[i].prices[lastIndex]
      strippedItem.price = currentPrice.price
      strippedItem.upvotes = currentPrice.upvotes
      strippedItem.downvotes = currentPrice.downvotes

      if (strippedItem.price < cheapestPrice) {
        cheapestPrice = strippedItem.price;
        cheapestItem = strippedItem;
      }
      newStores[storeName].items.push(strippedItem)
    }

    cheapestItem.cheapest = true;

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

  selectStore = (store) => {
    this.setState({
      selectedStore: store
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

  submitSearch = async (keyword, upc) => {
    if (!keyword || (keyword && keyword.trim() !== "")) {
      this.props.navigation.navigate("SearchResults", {keyword: keyword.trim(), upc: upc, handleAddItem: this.addItem})
    }
  }

  // This function will be called when a bar code is scanned, simply navigates to search results page
  handleBarCodeScanned = (type, data) => {
    this.submitSearch(null, data);
  }

  // This function is called when the scan button (camera button) is pressed
  scanBarCode = () => {
    this.props.navigation.navigate("Scan", {handleBarCodeScanned: this.handleBarCodeScanned})
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

  _onOpenCompare = () => {
    this.setState({isCollapsed: !this.state.isCollapsed});
  }


  render() {
    let TouchablePlatformSpecific = Platform.OS === 'ios' ? 
      TouchableHighlight : 
      TouchableNativeFeedback;
      
    if (this.state.selectedStore === '') {
      return (
        <View style={styles.container}>
          <ItemSearchBar onSearch={this.submitSearch} onPressCamera={this.scanBarCode}/>

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
                Component={TouchablePlatformSpecific}
                onLongPress={() => this.deleteAlert(i)}
                leftAvatar={{ title: l.name, source: { uri: l.imageUrl } }}
                title={l.name}
                rightTitle={'$' + Number(this.state.stores[this.state.selectedStore].items[i].price).toFixed(2)}
                rightTitleStyle={{color: this.state.stores[this.state.selectedStore].items[i].cheapest ? 'green': 'black'}}
                bottomDivider
              />
            ))}
          </View>

          <View style={styles.footer}>
            <Icon name={this.state.isCollapsed ? 'expand-less' : 'expand-more'} type='material'/>
            <ListItem
              title={'Total (' + this.state.stores[this.state.selectedStore].items.length + ' items)'}
              subtitle={this.state.selectedStore}
              rightTitle={'$' + Number(this.calculateStoreTotal(this.state.selectedStore)).toFixed(2)}
              topDivider
              onPress={this._onOpenCompare}
            />

            <Collapsible collapsed={this.state.isCollapsed} duration={100} style={{height: 140}}>
              <View style={styles.horizontalRow}>
              {Object.keys(this.state.stores).map((key, index) => (
                <View key={key}>
                  <Avatar
                    size="large"
                    overlayContainerStyle={this.state.selectedStore == key ? { borderWidth: 3, borderColor: 'green' } : { backgroundColor: '#BDBDBD' }}
                    rounded
                    onPress={() => this.selectStore(key)}
                    source={{
                      uri: storeLogos[key],
                    }}
                  />
                  {this.state.selectedStore == key &&
                    <Badge
                      status="success"
                      containerStyle={{ position: 'absolute', top: -2, right: -2 }}
                    />
                  }
                  <Text style={styles.subtitle}>
                    {'$' + Number(this.calculateStoreTotal(key)).toFixed(2)}
                  </Text>
                </View>
            ))} 
              </View>
            </Collapsible>
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
    )
   };
}

const storeLogos = {
  'Schnucks': 'https://d2d8wwwkmhfcva.cloudfront.net/195x/d2lnr5mha7bycj.cloudfront.net/warehouse/logo/216/9154d284-86de-4383-a73b-5779ace514f0.png',
  'Aldi': 'https://corporate.aldi.us/fileadmin/_processed_/7/6/csm_aldi_logo_2017_bd4f8371bc.jpg',
  'Harvest Market': 'https://scontent-ort2-2.xx.fbcdn.net/v/t31.0-8/13613392_151339761940766_246331264216770468_o.jpg?_nc_cat=103&_nc_ht=scontent-ort2-2.xx&oh=2d7694bfebaa768125b7be75ea4424b7&oe=5D412F44',
  'County Market': 'https://scontent-ort2-2.xx.fbcdn.net/v/t1.0-9/15803_580000272016261_661242806_n.jpg?_nc_cat=104&_nc_ht=scontent-ort2-2.xx&oh=6e3a82481fb7828bbee37ae90904dc65&oe=5D2B2E5F'
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
  },
  horizontalRow: {
    padding: 15, 
    flex: 1, 
    flexDirection: 'row', 
    justifyContent: 'space-evenly'
  },
  subtitle: {
    textAlign: 'center',
    paddingTop: 10
  }
});
