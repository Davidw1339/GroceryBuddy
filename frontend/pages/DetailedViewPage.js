import React, {Component} from 'react';
import {searchByUPC} from "../utils/api";
import { View, ActivityIndicator, StyleSheet} from 'react-native';

import { Image, PricingCard, Overlay, Text, Input, Button } from 'react-native-elements';


export default class DetailedViewPage extends Component {

    constructor(props) {
        super(props);
        this.state = {
            isLoading:true,
            priceOverlayVisible: false,
            newPrice: ''
        }
    }


    async componentDidMount() {
        let data = await searchByUPC(this.props.navigation.state.params.upc);
        this.setState({isLoading: false, ...data[0]})
    }

    toggleChangePriceOverlay = () => {
        this.setState(({priceOverlayVisible}) => ({
            priceOverlayVisible: !priceOverlayVisible
        }));
    }

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
        console.log(this.state);
        return (
          <View style={styles.DetailContainer}>
            <View style={styles.ItemImage}>
                <Image
                    PlaceholderContent={<ActivityIndicator />}
                    style={{ width: 300, height: 150 }}
                    source={{
                        uri:
                            this.state.image_url,
                    }} />
            </View>
            <View style={styles.priceContainer}>
                <PricingCard
                    color="#4f9deb"
                    title={this.state.name}
                    price={"$" + this.state.stores[0].prices[0].price.toString()}
                    info={["hot sale", "great deal", "amazing"]}
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
                        <Button containerStyle={styles.dialogButton} title="SUBMIT" onPress={this.addNewList} />
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
        justifyContent: 'center',
        alignItems: 'center'
    },
    ItemImage: {
        flex:1
    },
    priceContainer:{
        flex:0,

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