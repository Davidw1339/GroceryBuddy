import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Text } from 'react-native-elements';

export default class ShoppingPage extends React.Component {

    static navigationOptions = {
        title: 'Shopping Page',
    };

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <View style={styles.container}>
                <Text>Shopping Page</Text>
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