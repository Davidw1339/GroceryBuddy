import React from 'react';
import AddItemForm from '../components/AddItemForm';
import UPCScanner from '../components/UPCScanner';
import CameraView from '../components/CameraView';
import { createStackNavigator } from 'react-navigation';

const StackNav = createStackNavigator({
  Form: AddItemForm,
  Scanner: UPCScanner,
  Camera: {
    screen: CameraView,
    navigationOptions: {
      header: null
    }
  }
},
{
  headerMode: 'none',
  navigationOptions: {
    headerVisible: false,
  }
}
)

export default StackNav;