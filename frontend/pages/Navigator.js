import React from 'react';
import { createStackNavigator, createAppContainer } from 'react-navigation';
import SearchPage from './SearchPage';
import ListPage from './ListPage';
import AddItemPage from './AddItemPage';
import HomePage from './HomePage';
import SearchResultsPage from './SearchResultsPage';
import ShoppingPage from './ShoppingPage';
import DetailedViewPage from "./DetailedViewPage";

const ICON_SIZE = 25;

const StackNavigator = createStackNavigator({
  Home: {
    screen: HomePage
  },
  Search: {
    screen: SearchPage
  },
  SearchResults: {
    screen: SearchResultsPage
  },
  Shopping: {
    screen: ShoppingPage
  },
  AddItem: {
    screen: AddItemPage
  }
  Details: {
    screen:DetailedViewPage
  }
})

export default createAppContainer(StackNavigator);