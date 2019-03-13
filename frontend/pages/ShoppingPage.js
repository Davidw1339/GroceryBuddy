import React from 'react';
import { View, StyleSheet, TouchableNativeFeedback, Image } from 'react-native';
import { Text, CheckBox } from 'react-native-elements';
import { votePrice } from '../utils/api';
import { Ionicons, AntDesign } from '@expo/vector-icons';

export default class ShoppingPage extends React.Component {

  static navigationOptions = ({ navigation }) => {
    let listObj = navigation.getParam('list', {name: 'Shopping Page', store: ''})
    return {
      title: listObj.name + ' | ' + listObj.store
    };
  };

    username = 'developer';

    constructor(props) {
        super(props);
        console.log(props.navigation.getParam('list'));
        this.state = {
            list: props.navigation.getParam('list')
            //test: {name:'List 1', items: [{name: 'Apples', upc: '864498242575', price: 1.5, upvote: 15, downvote: 3, image: 'https://i5.walmartimages.ca/images/Large/428/5_r/6000195494285_R.jpg', quantity: 40}, {name: 'Apple Watch', price: 199.99, upvote: 1, downvote: 4, image: 'https://ss7.vzw.com/is/image/VerizonWireless/Apple_Watch_Series_4_GPS_Plus_Cellular_44mm_Aluminum_Case_with_Sport_Band_MTV02LLA?$png8alpha256$&hei=410', quantity: 1}], store: 'County Market'}
        }
    }

    display = (value, active) => {
        if (active) {
            return (value + 1);
        } else {
            return value;
        }
    }

    toggleUserInState = (state, arrayName, item, i) => {
        let newItem = {...item}
        if (newItem[arrayName] && newItem[arrayName].indexOf(this.username) > -1) {
            newItem[arrayName].splice(newItem[arrayName].indexOf(this.username), 1);
        } else {
            if (newItem[arrayName] === undefined) {
                newItem[arrayName] = [];
            }
            newItem[arrayName].push(this.username);
        }
        let newlist = [...state.list.items]
        newlist[i] = newItem
        let newState = {...state}
        newState.list.items = newlist
        return newState
    }

    upvotePrice = async (item, i) => {
        if (item.upvotes && item.upvotes.includes(this.username)) { // need to unupvote
            await votePrice(0, this.username, item.upc, {name: 'Schnucks', lat: 40.11695, long: -88.278297});
            let newState = this.toggleUserInState(this.state, "upvotes", item, i);
            this.setState((state) => {
                return newState
            });
        } 
        else {
            await votePrice(1, this.username, item.upc, {name: 'Schnucks', lat: 40.11695, long: -88.278297});
            let newState = this.state;
            if(item.downvotes && item.downvotes.includes(this.username)) { // need to get rid of downvote 
                newState = this.toggleUserInState(newState, "downvotes", item, i);
            }
            newState = this.toggleUserInState(newState, "upvotes", item, i);
            this.setState(newState);
        }
    }

    downvotePrice = async (item, i) => {
        if (item.downvotes && item.downvotes.includes(this.username)) { // need to unupvote
            await votePrice(0, this.username, item.upc, {name: 'Schnucks', lat: 40.11695, long: -88.278297});
            let newState = this.toggleUserInState(this.state, "downvotes", item, i);
            this.setState((state) => {
                return newState
            });
        } 
        else {
            await votePrice(-1, this.username, item.upc, {name: 'Schnucks', lat: 40.11695, long: -88.278297});
            let newState = this.state;
            if(item.upvotes && item.upvotes.includes(this.username)) { // need to get rid of upvote
                newState = this.toggleUserInState(newState, "upvotes", item, i);
            }
            newState = this.toggleUserInState(newState, "downvotes", item, i);
            this.setState(newState);
        }
    }

    render() {
        const list = this.state.list//this.props.navigation.getParam('list', {})
        console.log(list.name);
        return (
            <View style={styles.container}>
                {/* <Text style={styles.titleText}>{list.name} at {list.store}</Text> */}
                {list.items.map((list_item, i) => {
                        const checkState = "checked" + i;
                        const upState = "up" + i;
                        const downState = "down" + i;
                        return(
                            <View key={i} style={{flexDirection: 'row', alignItems: 'center', marginBottom: 20}}>
                                <CheckBox checked={this.state[checkState]} onPress={() => this.setState({[checkState]: !this.state[checkState]})}/>
                                <TouchableNativeFeedback style={styles.button} onPress={() => this.props.navigation.navigate('ItemDetails')}>
                                    <View style={{flex: 1, flexDirection: 'row'}}>
                                        <Image style={{width: 75, height: 75, marginRight: 20}} source={{uri: list_item.imageUrl}}/>
                                        <View style={{textAlign: 'center', flex: 1}}>
                                            <Text style={{fontSize: 20}} numberOfLines={2}>{list_item.name}</Text>
                                            <Text>Price: ${Number.parseFloat(list_item.price).toFixed(2)}</Text>
                                            <Text>Quantity: {list_item.quantity}</Text>
                                        </View>
                                    </View>
                                </TouchableNativeFeedback>
                                <View style={{marginLeft: 20, justifyContent: 'center'}}>
                                    <View style={{width: 100, flexDirection: 'row', justifyContent: 'center'}}>
                                        <TouchableNativeFeedback onPress={() => {
                                            this.upvotePrice(list_item, i)
                                            }}>
                                            <AntDesign name="caretup" size={24} color={list_item.upvotes && list_item.upvotes.includes(this.username) ? "green" : "black"}/>
                                        </TouchableNativeFeedback>
                                        <Text style={{marginLeft: 10, width: 20, textAlign: 'center'}}>{list_item.upvotes ? list_item.upvotes.length : 0}</Text>
                                    </View>
                                    <View style={{width: 100, flexDirection: 'row', justifyContent: 'center'}}>
                                        <TouchableNativeFeedback onPress={() => {
                                            this.downvotePrice(list_item, i)
                                            }}>
                                            <AntDesign name="caretdown" size={24} color={list_item.downvotes && list_item.downvotes.includes(this.username) ? "red": "black"}/>
                                        </TouchableNativeFeedback>
                                        <Text style={{marginLeft: 10, width: 20, textAlign: 'center'}}>{list_item.downvotes ? list_item.downvotes.length : 0}</Text>
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
        padding: 10
    },
    titleText: {
        fontSize: 24,
        textAlign: 'center',
        marginBottom: 20
    },
    button: {
        alignItems: 'center',
        backgroundColor: '#DDDDDD',
        padding: 10
    }
});
