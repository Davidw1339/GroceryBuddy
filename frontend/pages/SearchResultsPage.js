import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Text } from 'react-native-elements';

export default class SearchResultsPage extends React.Component {
    static navigationOptions = {
        title: 'Search Results Page',
    };

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <View style={styles.container}>
                <Text>Search Results Page</Text>
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
    }
});