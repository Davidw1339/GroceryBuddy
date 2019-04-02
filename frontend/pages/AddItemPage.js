import React from 'react';
import AddItemForm from '../components/AddItemForm';
import UPCScanner from '../components/UPCScanner';
import { createStackNavigator } from 'react-navigation';

const StackNav = createStackNavigator({
  Form: AddItemForm,
  Scanner: UPCScanner
},
{
  headerMode: 'none',
  navigationOptions: {
    headerVisible: false,
  }
}
)

export default StackNav;