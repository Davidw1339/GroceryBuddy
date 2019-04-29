// __tests__/Intro-test.js
import React from 'react';
import renderer from 'react-test-renderer';
import App from '../App';


test('renders correctly', () => {
  jest.useFakeTimers();
  const tree = renderer.create(<App />).toJSON();
  expect(tree).toMatchSnapshot('renders correctly');
});
