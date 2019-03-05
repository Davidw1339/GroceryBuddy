import React from 'react';
import { View, StyleSheet } from 'react-native';
import { Text, Button } from 'react-native-elements';

export default class HomePage extends React.Component {
    static navigationOptions = {
        title: 'Home',
    };

    constructor(props) {
        super(props);
    }

    render() {
        return (
            <View style={styles.container}>
                <Text>Home Page</Text>
                <Button
                    containerStyle={styles.button}
                    title="Go to search page"
                    onPress={() => {this.props.navigation.navigate("Search")}}
                />
                <Button
                    containerStyle={styles.button}
                    title="Go to search results page"
                    onPress={() => {this.props.navigation.navigate("SearchResults")}}
                />
                <Button
                    containerStyle={styles.button}
                    title="Go to shopping page"
                    onPress={() => {this.props.navigation.navigate("Shopping")}}
                />
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
    button: {
        margin: 5
    }
});