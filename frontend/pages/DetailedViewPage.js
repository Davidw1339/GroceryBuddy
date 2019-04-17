import React, {Component} from 'react';
import {searchByUPC} from "../utils/api";
import {View, ActivityIndicator, StyleSheet, FlatList} from 'react-native';
import _ from 'lodash'
import { Image, PricingCard, Overlay, Text, Input, Button } from 'react-native-elements';

export default class DetailedViewPage extends Component {
    constructor(props) {
        super(props);
        store = ''
        //Had to wrap this in a try catch for when the component is loaded with no navigation (testing)
        try {
            store = this.props.navigation.state.params.store
        } catch(err) {
            console.log(err)
        }
        this.state = {
            isLoading:true,
            priceOverlayVisible: false,
            newPrice: '',
            store: store
        }
    }

    async componentDidMount() {
        let data = await searchByUPC(this.props.navigation.state.params.upc);

        //we only want the prices for the store we selected
        currStore = this.state.store
        elem = data[0]
        stores = elem.stores
        res = _.find(stores, ['name', currStore])
        oldPrices = res.prices

        //add oldprices, as well as other item data, and let the app load
        this.setState({isLoading: false, oldPrices: oldPrices, ...data[0]})
    }

    toggleChangePriceOverlay = () => {
        this.setState(({priceOverlayVisible}) => ({
            priceOverlayVisible: !priceOverlayVisible
        }));
    }


    //TODO
    changePrice = () => {

    }

    render() {
        if (this.state.isLoading) {
            return (
                <View style={{flex: 1, alignContent: 'center', justifyContent: 'center'}}>
                    <ActivityIndicator/>
                </View>
            );
        }

        return (
          <View style={styles.DetailContainer}>
            <View style={styles.ItemImage}>
                <Image
                    PlaceholderContent={<ActivityIndicator />}
                    resizeMode='stretch'
                    style={{flex:1, width: 150, height: 150}}
                    source={{
                        uri:
                            this.state.image_url,
                    }} />
            </View>
            <View style={styles.HistoryContainer}>
                <View style={styles.HistoryHeader}>
                        <Text style={{ fontSize: 20, marginBottom: 0, paddingBottom: 0}}>History of prices at </Text>
                        <Text style={{ fontSize: 20, fontWeight: 'bold', marginBottom: 0, paddingBottom: 0}}>{this.state.store}:</Text>
                </View>
                <View style={{flex: 1}}>
                    <FlatList
                        data={this.state.oldPrices}
                        renderItem={({item}) => 
                            <View style={styles.OldPriceListItem}>
                                <Text style={{alignSelf: "flex-start"}}>{item.price.toString()}</Text>
                                <Text style={{ alignSelf: "flex-end", color: 'grey' }}>
                                    {((new Date(Math.floor(item.date) * 1000)).getMonth() + 1) + '/' + 
                                      (new Date(Math.floor(item.date) * 1000)).getDate() + '/' + 
                                      (new Date(Math.floor(item.date) * 1000)).getFullYear()}
                                </Text>
                            </View>}
                        keyExtractor={(item, index) => 'key' + index}
                    />
                </View>
            </View>
            <View style={styles.priceContainer}>
                <PricingCard
                    color="#4f9deb"
                    title={this.state.name}
                    price={"$" + this.state.oldPrices[0].price.toString()}
                    button={{ title: 'Add/Change Price', icon: 'add' }}
                    onButtonPress={this.toggleChangePriceOverlay}
                />
            </View>
            <Overlay
                isVisible={this.state.priceOverlayVisible}
                onBackdropPress={this.toggleAddListOverlay}
                animationType="fade"
                height={150}>
                <View style={styles.simpleContainer}>
                    <View style={styles.simpleContainer}>
                        <Text style={styles.button}>New Price:</Text>
                        <Input
                            value={this.state.newPrice}
                            onChangeText={(newPrice) => this.setState({newPrice})}
                            placeholder="$$$$"/>
                    </View>
                    <View style={styles.buttonGroup}>
                        <Button containerStyle={styles.dialogButton} title="CANCEL" onPress={this.toggleChangePriceOverlay} />
                        <Button containerStyle={styles.dialogButton} title="SUBMIT" onPress={this.toggleChangePriceOverlay} />
                    </View>
                </View>
            </Overlay>
          </View>
        );
    }
}

const styles = StyleSheet.create({
    DetailContainer: {
        flex:1,
        flexDirection: 'column',
        justifyContent: 'center', 
        alignItems: 'center'
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
        height: 30
    },
    OldPriceListItem: {
        flexDirection: 'row', 
        justifyContent: 'space-between', 
        paddingLeft: 10, 
        paddingRight: 10, 
        paddingBottom: 5
    },
    ItemImage: {
        flex:3,
        paddingTop: 5
    },
    priceContainer: {
        flex: 0,
    },
    simpleContainer: {
        flex: 1
    },
    dialogButton: {
        flex: 1,
        margin: 5,
        borderRadius: 100
    },
    button: {
        margin: 5
    },
    buttonGroup: {
        flexDirection: "row"
    },
});