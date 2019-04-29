import React from 'react';
import {
  View, StyleSheet, TouchableNativeFeedback, TouchableHighlight, Image,
  Platform,
} from 'react-native';
import { Text, CheckBox } from 'react-native-elements';
import { AntDesign } from '@expo/vector-icons';
import { votePrice, getUserId } from '../utils/api';

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#fff',
    padding: 10,
  },
  titleText: {
    fontSize: 24,
    textAlign: 'center',
    marginBottom: 20,
  },
  button: {
    alignItems: 'center',
    backgroundColor: '#DDDDDD',
    padding: 10,
  },
  itemName: {
    fontSize: 20,
  },
  item: {
    textAlign: 'center',
    flex: 1,
  },
  image: {
    width: 75,
    height: 75,
    marginRight: 20,
  },
  itemDetailsContainer: {
    flex: 1,
    flexDirection: 'row',
  },
  itemContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 20,
  },
  voteButton: {
    marginLeft: 10,
    width: 20,
    textAlign: 'center',
  },
  voteContainer: {
    width: 100,
    flexDirection: 'row',
    justifyContent: 'center',
  },
  vote: {
    marginLeft: 20,
    justifyContent: 'center',
  },
});

export default class ShoppingPage extends React.Component {
    static navigationOptions = ({ navigation }) => {
      const listObj = navigation.getParam('list', { name: 'Shopping Page', store: '' });
      return {
        title: `${listObj.name} | ${listObj.store}`,
      };
    };

    constructor(props) {
      super(props);
      this.state = {
        list: props.navigation.getParam('list'),
      };
    }

    componentDidMount() {
      this.setUserId();
    }

    setUserId = async () => {
      const userid = await getUserId();
      this.setState({ username: userid });
    }

    display = (value, active) => {
      if (active) {
        return (value + 1);
      }
      return value;
    }

    toggleUserInState = (state, arrayName, item, i) => {
      const newItem = { ...item };
      if (newItem[arrayName] && newItem[arrayName].indexOf(this.state.username) > -1) {
        newItem[arrayName].splice(newItem[arrayName].indexOf(this.state.username), 1);
      } else {
        if (newItem[arrayName] === undefined) {
          newItem[arrayName] = [];
        }
        newItem[arrayName].push(this.state.username);
      }
      const newlist = [...state.list.items];
      newlist[i] = newItem;
      const newState = { ...state };
      newState.list.items = newlist;
      return newState;
    }

    upvotePrice = async (item, i) => {
      const { store, lat, long } = this.state.list;
      const storeInfo = {
        name: store,
        lat,
        long,
      };
      if (item.upvotes && item.upvotes.includes(this.state.username)) { // need to unupvote
        await votePrice(0, this.state.username, item.upc, storeInfo);
        const newState = this.toggleUserInState(this.state, 'upvotes', item, i);
        this.setState(() => newState);
      } else {
        await votePrice(1, this.state.username, item.upc, storeInfo);
        let newState = this.state;
        if (item.downvotes && item.downvotes.includes(this.state.username)) { // get rid of downvote
          newState = this.toggleUserInState(newState, 'downvotes', item, i);
        }
        newState = this.toggleUserInState(newState, 'upvotes', item, i);
        this.setState(newState);
      }
    }

    downvotePrice = async (item, i) => {
      const { store, lat, long } = this.state.list;
      const storeInfo = {
        name: store,
        lat,
        long,
      };
      if (item.downvotes && item.downvotes.includes(this.state.username)) { // need to unupvote
        await votePrice(0, this.state.username, item.upc, storeInfo);
        const newState = this.toggleUserInState(this.state, 'downvotes', item, i);
        this.setState(() => newState);
      } else {
        await votePrice(-1, this.state.username, item.upc, storeInfo);

        let newState = this.state;
        if (item.upvotes && item.upvotes.includes(this.state.username)) { // get rid of upvote
          newState = this.toggleUserInState(newState, 'upvotes', item, i);
        }
        newState = this.toggleUserInState(newState, 'downvotes', item, i);
        this.setState(newState);
      }
    }

    render() {
      const { list } = this.state;

      const TouchablePlatformSpecific = Platform.OS === 'ios'
        ? TouchableHighlight
        : TouchableNativeFeedback;

      return (
        <View style={styles.container}>
          {list.items.map((listItem, i) => {
            const checkState = `checked${i}`;
            return (
              <View key={listItem.upc + i} style={styles.itemContainer}>
                <CheckBox
                  checked={this.state[checkState]}
                  onPress={() => this.setState(state => ({ [checkState]: !state[checkState] }))}
                />
                <TouchablePlatformSpecific style={styles.button} onPress={() => this.props.navigation.navigate('Details', { upc: listItem.upc, store: this.state.list.store })}>
                  <View style={styles.itemDetailsContainer}>
                    <Image style={styles.image} source={{ uri: listItem.imageUrl }} />
                    <View style={styles.item}>
                      <Text style={styles.itemName} numberOfLines={2}>{listItem.name}</Text>
                      <Text>
                        Price: $
                        {Number.parseFloat(listItem.price).toFixed(2)}
                      </Text>
                      <Text>
                        Quantity:
                        {' '}
                        {listItem.quantity}
                      </Text>
                    </View>
                  </View>
                </TouchablePlatformSpecific>
                <View style={styles.vote}>
                  <View style={styles.voteContainer}>
                    <TouchablePlatformSpecific onPress={() => {
                      this.upvotePrice(listItem, i);
                    }}
                    >
                      <AntDesign name="caretup" size={24} color={listItem.upvotes && listItem.upvotes.includes(this.state.username) ? 'green' : 'black'} />
                    </TouchablePlatformSpecific>
                    <Text style={styles.voteButton}>
                      {listItem.upvotes ? listItem.upvotes.length : 0}
                    </Text>
                  </View>
                  <View style={styles.voteContainer}>
                    <TouchablePlatformSpecific onPress={() => {
                      this.downvotePrice(listItem, i);
                    }}
                    >
                      <AntDesign name="caretdown" size={24} color={listItem.downvotes && listItem.downvotes.includes(this.state.username) ? 'red' : 'black'} />
                    </TouchablePlatformSpecific>
                    <Text style={styles.voteButton}>
                      {listItem.downvotes ? listItem.downvotes.length : 0}
                    </Text>
                  </View>
                </View>
              </View>
            );
          })}
        </View>
      );
    }
}
