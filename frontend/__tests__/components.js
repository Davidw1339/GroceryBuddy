


// __tests__/Intro-test.js
import React from 'react';

import renderer from 'react-test-renderer';
import AddItemForm from "../components/AddItemForm";
import ItemSearchBar from "../components/ItemSearchBar";
import ItemView from "../components/ItemView";
import ListItem from "../components/ListItem";
import ItemAdditionForm from "../components/UPCScanner";

test('AddItemForm', () => {
    jest.useFakeTimers();
    const tree = renderer.create(<AddItemForm />).toJSON();
    expect(tree).toMatchSnapshot();
});

test('ItemSearchBar', () => {
    jest.useFakeTimers();
    const tree = renderer.create(<ItemSearchBar />).toJSON();
    expect(tree).toMatchSnapshot();
});

test('ListItem', () => {
    jest.useFakeTimers();
    const tree = renderer.create(<ListItem />).toJSON();
    expect(tree).toMatchSnapshot();
});


test('UPCScanner', () => {
    jest.useFakeTimers();
    const tree = renderer.create(<ItemAdditionForm />).toJSON();
    expect(tree).toMatchSnapshot();
});

