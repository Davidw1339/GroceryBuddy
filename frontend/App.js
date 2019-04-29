import React from 'react';
import { YellowBox } from 'react-native';
import Navigator from './pages/Navigator';

export default class App extends React.Component {
  componentWillMount() {
    YellowBox.ignoreWarnings(['Require cycle:']);
  }

  render() {
    return (
      <Navigator />
    );
  }
}
