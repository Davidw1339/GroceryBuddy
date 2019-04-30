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

/**
 * Class representing home page
 * @extends React.Component
 */
export default class HomePage extends React.Component {
    static navigationOptions = {
      title: 'Lists',
    }

    /**
     * Creates the HomePage
     * @param {object} props
     */
    constructor(props) {
      super(props);
      this.state = {
        lists: [],
        listOverlayVisible: false,
        newListName: '',
      };
    }

    /**
     * Fetches the initial lists
     */
    componentDidMount() {
      this.retrieveLists();
    }

    /**
     * Retrieves lists from async stoage
     */
    retrieveLists = async () => {
      const lists = await getLists();
      this.setState({
        lists,
      });
    }

    /**
     * Toggles the overlay/modal for creating new list
     */
    toggleAddListOverlay = () => {
      this.setState(({ listOverlayVisible }) => ({
        listOverlayVisible: !listOverlayVisible,
      }));
    }

    /**
     * Adds a new list to the set of lists
     */
    addNewList = async () => {
      this.toggleAddListOverlay(); // close the modal
      this.setState({ newListName: '' }); // clear our the modal input
      await addList(this.state.lists, this.state.newListName); // add the new list
      this.retrieveLists(); // refresh the set of lists on the homepage
    }

    /**
     * Deletes a list from the list page
     * @param  {number} id - the id of the list
     */
    deleteList = async (id) => {
      await deleteList(this.state.lists, id);
      this.retrieveLists();
    }

    /**
     * Launches the search/list page
     * @param  {string} name - the name of the list
     */
    launchList = (name) => {
      this.props.navigation.navigate('Search', { name });
    }

    /**
    * Renders home page.
    * @return {View} The home page.
    */
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
