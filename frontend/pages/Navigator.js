import { createStackNavigator, createAppContainer } from 'react-navigation';
import SearchPage from './SearchPage';
import UPCScanner from '../components/UPCScanner';
import AddItemPage from './AddItemPage';
import HomePage from './HomePage';
import SearchResultsPage from './SearchResultsPage';
import ShoppingPage from './ShoppingPage';
import DetailedViewPage from './DetailedViewPage';

const StackNavigator = createStackNavigator({
  Home: {
    screen: HomePage,
  },
  Search: {
    screen: SearchPage,
  },
  SearchResults: {
    screen: SearchResultsPage,
  },
  Shopping: {
    screen: ShoppingPage,
  },
  AddItem: {
    screen: AddItemPage,
    navigationOptions: {
      title: 'Add Item',
    },
  },
  Details: {
    screen: DetailedViewPage,
  },
  Scan: {
    screen: UPCScanner,
  },
});

export default createAppContainer(StackNavigator);
