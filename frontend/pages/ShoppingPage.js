import React from 'react';
import { View, StyleSheet, TouchableNativeFeedback, TouchableHighlight, Image } from 'react-native';
import { Text, CheckBox } from 'react-native-elements';
import { votePrice, getUserId } from '../utils/api';
import { Ionicons, AntDesign } from '@expo/vector-icons';
import { Platform } from 'react-native'

export default class ShoppingPage extends React.Component {

    static navigationOptions = ({ navigation }) => {
        let listObj = navigation.getParam('list', { name: 'Shopping Page', store: '' });
        return {
            title: listObj.name + ' | ' + listObj.store
        };
    };

    //Decided not to have users login, still need a unique identifier for downvotes to work
    // username = DeviceInfo.getMACAddress();

    constructor(props) {
        super(props);
        this.state = {
            list: props.navigation.getParam('list')
        }
    }

    componentDidMount() {
        this.setUserId()
    }

    setUserId = async () => {
        const userid = await getUserId();
        this.setState({ username: userid })
    }

    display = (value, active) => {
        if (active) {
            return (value + 1);
        } else {
            return value;
        }
    }

    toggleUserInState = (state, arrayName, item, i) => {
        let newItem = { ...item }
        if (newItem[arrayName] && newItem[arrayName].indexOf(this.username) > -1) {
            newItem[arrayName].splice(newItem[arrayName].indexOf(this.username), 1);
        } else {
            if (newItem[arrayName] === undefined) {
                newItem[arrayName] = [];
            }
            newItem[arrayName].push(this.state.username);
        }
        let newlist = [...state.list.items];
        newlist[i] = newItem;
        let newState = { ...state };
        newState.list.items = newlist;
        return newState;
    }

    upvotePrice = async (item, i) => {
        const {store, lat, long} = this.state.list;
        const storeInfo = {
            name: store,
            lat,
            long
        }
        if (item.upvotes && item.upvotes.includes(this.state.username)) { // need to unupvote
            await votePrice(0, this.state.username, item.upc, storeInfo);
            let newState = this.toggleUserInState(this.state, "upvotes", item, i);
            this.setState((state) => {
                return newState;
            });
        }
        else {
            await votePrice(1, this.state.username, item.upc, storeInfo);
            let newState = this.state;
            if(item.downvotes && item.downvotes.includes(this.state.username)) { // need to get rid of downvote 
                newState = this.toggleUserInState(newState, "downvotes", item, i);
            }
            newState = this.toggleUserInState(newState, "upvotes", item, i);
            this.setState(newState);
        }
    }

    downvotePrice = async (item, i) => {
        const {store, lat, long} = this.state.list;
        const storeInfo = {
            name: store,
            lat,
            long
        }
        if (item.downvotes && item.downvotes.includes(this.state.username)) { // need to unupvote
            await votePrice(0, this.state.username, item.upc, storeInfo);
            let newState = this.toggleUserInState(this.state, "downvotes", item, i);
            this.setState((state) => {
                return newState;
            });
        }
        else {
            await votePrice(-1, this.state.username, item.upc, storeInfo);

            let newState = this.state;
            if(item.upvotes && item.upvotes.includes(this.state.username)) { // need to get rid of upvote
                newState = this.toggleUserInState(newState, "upvotes", item, i);
            }
            newState = this.toggleUserInState(newState, "downvotes", item, i);
            this.setState(newState);
        }
    }

    render() {
        const list = this.state.list



        return (
            <View style={styles.container}>
                {list.items.map((list_item, i) => {

                    const checkState = "checked" + i;
                    const upState = "up" + i;
                    const downState = "down" + i;
                    return <ShoppingItem
                        list_item={list_item}
                        index={i}
                        isChecked={(key) => this.state[key]}
                        upvoteFunc={this.upvotePrice}
                        downvoteFunc={this.downvotePrice}
                        key={i}
                        username={this.state.username}
                        goToDetails={() => this.props.navigation.navigate('Details', { upc: list_item.upc, store: this.state.list.store })} />
                })}
            </View>
        );
    }
}

class ShoppingItem extends React.Component {

    render() {
        list_item = this.props.list_item
        i = this.props.index
        const checkState = "checked" + i
        isChecked = this.props.isChecked(checkState)
        upvoteFunc = () => { this.props.upvoteFunc(list_item, i) }
        downvoteFunc = () => { this.props.downvoteFunc(list_item, i) }
        username = this.props.username
        goToDetails = this.props.goToDetails

        let TouchablePlatformSpecific = Platform.OS === 'ios' ?
            TouchableHighlight :
            TouchableNativeFeedback;

        console.log(username)
        return (
            <View key={i} style={styles.itemContainer}>
                <CheckBox checked={isChecked} onPress={() => this.setState({ [checkState]: !this.state[checkState] })} />
                <TouchablePlatformSpecific style={styles.button} onPress={goToDetails}>
                    <View style={styles.itemDetailsContainer}>
                        <Image style={styles.image} source={{ uri: list_item.imageUrl }} />
                        <View style={styles.item}>
                            <Text style={styles.itemName} numberOfLines={2}>{list_item.name}</Text>
                            <Text>Price: ${Number.parseFloat(list_item.price).toFixed(2)}</Text>
                            <Text>Quantity: {list_item.quantity}</Text>
                        </View>
                    </View>
                </TouchablePlatformSpecific>
                <View style={styles.vote}>
                    <View style={styles.voteContainer}>
                        <TouchablePlatformSpecific onPress={upvoteFunc}>
                            <AntDesign name="caretup" size={24} color={list_item.upvotes && list_item.upvotes.includes(username) ? "green" : "black"} />
                        </TouchablePlatformSpecific>
                        <Text style={styles.voteButton}>{list_item.upvotes ? list_item.upvotes.length : 0}</Text>
                    </View>
                    <View style={styles.voteContainer}>
                        <TouchablePlatformSpecific onPress={downvoteFunc}>
                            <AntDesign name="caretdown" size={24} color={list_item.downvotes && list_item.downvotes.includes(username) ? "red" : "black"} />
                        </TouchablePlatformSpecific>
                        <Text style={styles.voteButton} >{list_item.downvotes ? list_item.downvotes.length : 0}</Text>
                    </View>
                </View>
            </View>)

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
    },
    itemName: {
        fontSize: 20
    },
    item: {
        textAlign: 'center',
        flex: 1
    },
    image: {
        width: 75,
        height: 75,
        marginRight: 20
    },
    itemDetailsContainer: {
        flex: 1,
        flexDirection: 'row'
    },
    itemContainer: {
        flexDirection: 'row',
        alignItems: 'center',
        marginBottom: 20
    },
    voteButton: {
        marginLeft: 10,
        width: 20,
        textAlign: 'center'
    },
    voteContainer: {
        width: 100,
        flexDirection: 'row',
        justifyContent: 'center'
    },
    vote: {
        marginLeft: 20,
        justifyContent: 'center'
    }
});
