import React, {Component} from 'react';
import {searchByUPC} from "../utils/api";
import { View, ActivityIndicator, StyleSheet} from 'react-native';

import { Image, PricingCard } from 'react-native-elements';


export default class DetailedViewPage extends Component {

    constructor(props) {
        super(props);
        this.state = {isLoading:true}
    }


    async componentDidMount() {
        let data = await searchByUPC(this.props.navigation.state.params.upc);
        this.setState({isLoading: false, ...data[0]})
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
                        style={{ width: 300, height: 150}}
                        source={{
                            uri:
                                this.state.image_url,
                        }}/>
                </View>
              <View style={styles.priceContainer}>
                  <PricingCard
                      color="#4f9deb"
                      title={this.state.name}
                      price={"$"+this.state.stores[0].prices[0].price.toString()}
                      info={["hot sale", "great deal", "amazing"]}
                      button={{ title: 'Just Do It', icon: 'add'}}
                  />
              </View>
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

    }
});