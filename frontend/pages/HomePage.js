import React from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import {
  Text, Button, Overlay, Input,
} from 'react-native-elements';
import ActionButton from 'react-native-action-button';
import ListItem from '../components/ListItem';
import { getLists, addList, deleteList } from '../utils/api';

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#f4f4f4',
    padding: 10,
  },
  button: {
    margin: 5,
  },
  scrollView: {
    flex: 1,
  },
  simpleContainer: {
    flex: 1,
  },
  buttonGroup: {
    flexDirection: 'row',
  },
  dialogButton: {
    flex: 1,
    margin: 5,
    borderRadius: 100,
  },
});

export default class HomePage extends React.Component {
    static navigationOptions = {
      title: 'Lists',
    }

    constructor(props) {
      super(props);
      this.state = {
        lists: [],
        listOverlayVisible: false,
        newListName: '',
      };
    }

    componentDidMount() {
      this.retrieveLists();
    }

    retrieveLists = async () => {
      const lists = await getLists();
      this.setState({
        lists,
      });
    }

    toggleAddListOverlay = () => { // toggles the overlay/modal for creating new list
      this.setState(({ listOverlayVisible }) => ({
        listOverlayVisible: !listOverlayVisible,
      }));
    }

    addNewList = async () => {
      this.toggleAddListOverlay(); // close the modal
      this.setState({ newListName: '' }); // clear our the modal input
      await addList(this.state.lists, this.state.newListName); // add the new list
      this.retrieveLists(); // refresh the set of lists on the homepage
    }

    deleteList = async (id) => {
      await deleteList(this.state.lists, id);
      this.retrieveLists();
    }

    launchList = (name) => {
      this.props.navigation.navigate('Search', { name });
    }

    render() {
      return (
        <View style={styles.container}>
          {/* Render all list items */}
          <ScrollView style={styles.scrollView}>
            {this.state.lists.map(({ name }, i) => (
              <ListItem
                key={name + i}
                name={name}
                handleDelete={() => { this.deleteList(i); }}
                handleLaunchList={() => { this.launchList(name); }}
              />
            ))}
          </ScrollView>
          <ActionButton buttonColor="#2196f3" onPress={this.toggleAddListOverlay} />

          {/* This overlay is shown to read in user input and create a new list */}
          <Overlay
            isVisible={this.state.listOverlayVisible}
            onBackdropPress={this.toggleAddListOverlay}
            animationType="fade"
            height={150}
          >
            <View style={styles.simpleContainer}>
              <View style={styles.simpleContainer}>
                <Text style={styles.button}>Name of List:</Text>
                <Input
                  value={this.state.newListName}
                  onChangeText={newListName => this.setState({ newListName })}
                  placeholder="List Name"
                />
              </View>
              <View style={styles.buttonGroup}>
                <Button containerStyle={styles.dialogButton} title="CANCEL" onPress={this.toggleAddListOverlay} />
                <Button containerStyle={styles.dialogButton} title="ADD" onPress={this.addNewList} />
              </View>
            </View>
          </Overlay>
        </View>
      );
    }
}
