import React, { Component } from 'react';
import {
  View, ActivityIndicator, StyleSheet, FlatList,
} from 'react-native';
import _ from 'lodash';
import {
  Image, PricingCard, Overlay, Text, Input, Button,
} from 'react-native-elements';
import { addPrice, searchByUPC } from '../utils/api';

const styles = StyleSheet.create({
  DetailContainer: {
    flex: 1,
    flexDirection: 'column',
    justifyContent: 'center',
    alignItems: 'center',
  },
  HistoryContainer: {
    flex: 2,
    width: '100%',
  },
  HistoryHeader: {
    flexDirection: 'row',
    paddingLeft: 5,
    paddingRight: 5,
    marginBottom: 0,
    paddingBottom: 0,
    height: 30,
  },
  OldPriceListItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingLeft: 10,
    paddingRight: 10,
    paddingBottom: 5,
  },
  ItemImage: {
    flex: 3,
    paddingTop: 5,
  },
  priceContainer: {
    flex: 0,
  },
  simpleContainer: {
    flex: 1,
  },
  dialogButton: {
    flex: 1,
    margin: 5,
    borderRadius: 100,
  },
  button: {
    margin: 5,
  },
  buttonGroup: {
    flexDirection: 'row',
  },
  activityMonitor: {
    flex: 1,
    alignContent: 'center',
    justifyContent: 'center',
  },
});

export default class DetailedViewPage extends Component {
  constructor(props) {
    super(props);
    let store = '';

    try {
      ({ store } = this.props.navigation.state.params);
    } catch (err) {
      // Had to wrap this in a try catch for when the component is
      // loaded with no navigation (testing)
    }
    this.state = {
      isLoading: true,
      priceOverlayVisible: false,
      newPrice: '',
      store,
    };
  }

  async componentDidMount() {
    this.refresh();
  }

    refresh = async () => {
      const data = await searchByUPC(this.props.navigation.state.params.upc);

      // we only want the prices for the store we selected
      const currStore = this.state.store;
      const elem = data[0];
      const { stores } = elem;
      const res = _.find(stores, ['name', currStore]);
      const oldPrices = res.prices;

      // add oldprices, as well as other item data, and let the app load
      this.setState({ isLoading: false, oldPrices, ...data[0] });
    }

    toggleChangePriceOverlay = () => {
      this.setState(({ priceOverlayVisible }) => ({
        priceOverlayVisible: !priceOverlayVisible,
      }));
    }

    changePrice = async () => {
      /*
            Find the first store that matches the store selected by the user to
            get the location data from it.
         */
      const { navigation } = this.props;
      const navProps = navigation.state.params;
      const storeName = navProps.store;
      let lat = 0;
      let long = 0;
      // we choose to use the 'of' keyword over a clunkier foreach
      // eslint-disable-next-line no-restricted-syntax
      for (const store of this.state.stores) {
        if (store.name === storeName) {
          ({ lat, long } = store.location);
        }
      }
      this.setState(state => ({ ...state, isLoading: true }));
      await addPrice({
        upc: this.state.upc,
        price: parseFloat(this.state.newPrice),
        user: 'user',
        store: storeName,
        lat: parseFloat(lat),
        long: parseFloat(long),
      });
      this.refresh();
      this.toggleChangePriceOverlay();
    }

    render() {
      if (this.state.isLoading) {
        return (
          <View style={styles.activityMonitor}>
            <ActivityIndicator />
          </View>
        );
      }

      return (
        <View style={styles.DetailContainer}>
          <View style={styles.ItemImage}>
            <Image
              PlaceholderContent={<ActivityIndicator />}
              resizeMode="stretch"
              style={{ flex: 1, width: 150, height: 150 }}
              source={{
                uri:
                            this.state.image_url,
              }}
            />
          </View>
          <View style={styles.HistoryContainer}>
            <View style={styles.HistoryHeader}>
              <Text style={{ fontSize: 20, marginBottom: 0, paddingBottom: 0 }}>
                History of prices at
              </Text>
              <Text style={{
                fontSize: 20, fontWeight: 'bold', marginBottom: 0, paddingBottom: 0,
              }}
              >
                {this.state.store}
:
              </Text>
            </View>
            <View style={{ flex: 1 }}>
              <FlatList
                data={this.state.oldPrices}
                renderItem={({ item }) => (
                  <View style={styles.OldPriceListItem}>
                    <Text style={{ alignSelf: 'flex-start' }}>
                      $
                      {item.price.toFixed(2)}
                    </Text>
                    <Text style={{ alignSelf: 'flex-end', color: 'grey' }}>
                      {`${(new Date(Math.floor(item.date) * 1000)).getMonth() + 1}/${
                        (new Date(Math.floor(item.date) * 1000)).getDate()}/${
                        (new Date(Math.floor(item.date) * 1000)).getFullYear()}`}
                    </Text>
                  </View>
                )}
                keyExtractor={(item, index) => `key${index}`}
              />
            </View>
          </View>
          <View style={styles.priceContainer}>
            <PricingCard
              color="#4f9deb"
              title={this.state.name}
              price={`$${this.state.oldPrices[this.state.oldPrices.length - 1].price.toFixed(2)}`}
              button={{ title: 'Add/Change Price', icon: 'add' }}
              onButtonPress={this.toggleChangePriceOverlay}
            />
          </View>
          <Overlay
            isVisible={this.state.priceOverlayVisible}
            onBackdropPress={this.toggleAddListOverlay}
            animationType="fade"
            height={150}
          >
            <View style={styles.simpleContainer}>
              <View style={styles.simpleContainer}>
                <Text style={styles.button}>New Price:</Text>
                <Input
                  value={this.state.newPrice}
                  onChangeText={newPrice => this.setState({ newPrice })}
                  placeholder="$$$$"
                />
              </View>
              <View style={styles.buttonGroup}>
                <Button containerStyle={styles.dialogButton} title="CANCEL" onPress={this.toggleChangePriceOverlay} />
                <Button containerStyle={styles.dialogButton} title="SUBMIT" onPress={this.changePrice} />
              </View>
            </View>
          </Overlay>
        </View>
      );
    }
}
