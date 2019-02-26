import React from 'react';
import { Ionicons } from '@expo/vector-icons';
import { createBottomTabNavigator, createAppContainer } from 'react-navigation';
import SearchPage from './SearchPage';
import ListPage from './ListPage';
import AddItemPage from './AddItemPage';

const ICON_SIZE = 25;

const TabNavigator = createBottomTabNavigator({
  SEARCH: SearchPage,
  LIST: ListPage,
  ADD: AddItemPage
},
{
  defaultNavigationOptions: ({ navigation }) => ({
    tabBarIcon: ({focused, horizontal, tintColor }) => {
        const { routeName } = navigation.state;
        
        if (routeName === 'SEARCH') {
          return <Ionicons name="ios-search" size={ICON_SIZE} color={tintColor} />;
        }
        else if (routeName === 'LIST') {
          return <Ionicons name="ios-list" size={ICON_SIZE} color={tintColor} />;
        }
        else if (routeName === 'ADD') {
          return <Ionicons name="ios-add" size={ICON_SIZE} color={tintColor} />;
        }
    },
  }),
  tabBarOptions: {
    activeBackgroundColor: '#4288d6',
    activeTintColor: 'white',
    inactiveTintColor: 'gray',
    labelStyle: {
      fontSize: 12,
    },
    tabStyle: {
    },
    style: {
      shadowColor: 'transparent',
    }
  }
});


export default createAppContainer(TabNavigator);