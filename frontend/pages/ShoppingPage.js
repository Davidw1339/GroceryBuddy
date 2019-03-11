import React from 'react';
import { View, StyleSheet, TouchableNativeFeedback, Image } from 'react-native';
import { Text, CheckBox } from 'react-native-elements';
import { Ionicons } from '@expo/vector-icons';

export default class ShoppingPage extends React.Component {

    static navigationOptions = {
        title: 'Shopping Page',
    };

    constructor(props) {
        super(props);
        this.state = {
            test: {name:'List 1', items: [{name: 'Apples', price: 1.5, upvote: 15, downvote: 3, image: 'https://i5.walmartimages.ca/images/Large/428/5_r/6000195494285_R.jpg', quantity: 40}, {name: 'Apple Watch', price: 199.99, upvote: 1, downvote: 4, image: 'https://ss7.vzw.com/is/image/VerizonWireless/Apple_Watch_Series_4_GPS_Plus_Cellular_44mm_Aluminum_Case_with_Sport_Band_MTV02LLA?$png8alpha256$&hei=410', quantity: 1}], store: 'County Market'}
        }
    }

    display = (value, active) => {
        if (active) {
            return (value + 1);
        } else {
            return value;
        }
    }

    render() {
        const list = this.state.test//this.props.navigation.getParam('list', {})
        return (
            <View style={styles.container}>
                <Text style={styles.titleText}>{list.name} at {list.store}</Text>
                {list.items.map((list_item, i) => {
                        const checkState = "checked" + i;
                        const upState = "up" + i;
                        const downState = "down" + i;
                        return(
                            <View key={i} style={{flexDirection: 'row'}}>
                                <CheckBox checked={this.state[checkState]} onPress={() => this.setState({[checkState]: !this.state[checkState]})}/>
                                <TouchableNativeFeedback style={styles.button} onPress={() => this.props.navigation.navigate('ItemDetails')}>
                                    <View style={{flexDirection: 'row'}}>
                                        <Image style={{width: 75, height: 75, marginRight: 20}} source={{uri: list_item.image}}/>
                                        <View style={{textAlign: 'center'}}>
                                            <Text style={{fontSize: 20}}>{list_item.name}</Text>
                                            <Text>Price: ${Number.parseFloat(list_item.price).toFixed(2)}</Text>
                                            <Text>Quantity: {list_item.quantity}</Text>
                                        </View>
                                    </View>
                                </TouchableNativeFeedback>
                                <View style={{marginLeft: 20, justifyContent: 'center'}}>
                                    <View style={{flexDirection: 'row'}}>
                                        <TouchableNativeFeedback onPress={() => {
                                            if(!this.state[upState] && this.state[downState]) {
                                                this.setState({[upState]: !this.state[upState]});
                                                this.setState({[downState]: !this.state[downState]});
                                            } else {
                                                this.setState({[upState]: !this.state[upState]});
                                            }}}>
                                            <Ionicons name="md-arrow-up" size={24} color={"black"}/>
                                        </TouchableNativeFeedback>
                                        <Text>{this.display(list_item.upvote, this.state[upState])}</Text>
                                    </View>
                                    <View style={{flexDirection: 'row'}}>
                                        <TouchableNativeFeedback onPress={() => {
                                            if(this.state[upState] && !this.state[downState]) {
                                                this.setState({[upState]: !this.state[upState]});
                                                this.setState({[downState]: !this.state[downState]});
                                            } else {
                                                this.setState({[downState]: !this.state[downState]});
                                            }}}>
                                            <Ionicons name="md-arrow-down" size={24} color={"black"}/>
                                        </TouchableNativeFeedback>
                                        <Text>{this.display(list_item.downvote, this.state[downState])}</Text>
                                    </View>
                                </View>
                            </View>
                        )
                })}
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
    titleText: {
        fontSize: 30,
        fontWeight: 'bold',
        textAlign: 'center',
        marginBottom: 20
    },
    button: {
        alignItems: 'center',
        backgroundColor: '#DDDDDD',
        padding: 10
    }
});
