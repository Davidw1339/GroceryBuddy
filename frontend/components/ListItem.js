'use strict';

import React, { Component } from 'react'
import { StyleSheet, View, TouchableOpacity, TouchableNativeFeedback } from 'react-native';
import { Card, Text } from 'react-native-elements';
import Icons from '@expo/vector-icons/FontAwesome';

/**
 * ListItem describes a clickable list element that is displayed on the homepage
 */
export default class ListItem extends Component {

    render() {
        return (
            <TouchableNativeFeedback>
                <Card containerStyle={styles.card}>
                    <View style={styles.cardContentContainer}>
                        <Text style={styles.cardText}>{this.props.name}</Text>
                        <View style={styles.cardControlContainer}>
                            <TouchableOpacity style={styles.cardControl}>
                                <Icons name="pencil" size={24} color="gray" />
                            </TouchableOpacity>
                            <TouchableOpacity style={styles.cardControl} onPress={this.props.handleDelete}>
                                <Icons name="trash-o" size={24} color="gray" />
                            </TouchableOpacity>
                        </View>
                    </View>
                </Card>
            </TouchableNativeFeedback>
        );
    }
}

const styles = StyleSheet.create({
    container: {
        marginTop: 65
    },
    card: {
        padding: 10,
        borderRadius: 10
    },
    cardControlContainer: {
        alignItems: 'center',
        justifyContent: 'center'
    },
    cardControl: {
        margin: 10
    },
    cardText: {
        flex: 1,
        marginLeft: 20,
        fontSize: 18,
        fontWeight: "bold"
    },
    cardContentContainer: { 
        flex: 1, 
        lexDirection: 'row', 
        alignItems: 'center' 
    }
});