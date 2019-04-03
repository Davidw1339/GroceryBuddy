import React from 'react';
import renderer from "react-test-renderer";
import DetailedViewPage from "../pages/DetailedViewPage";
import HomePage from "../pages/HomePage";
import SearchPage from "../pages/SearchPage";
import SearchResultsPage from "../pages/SearchResultsPage";
import ShoppingPage from "../pages/ShoppingPage";



test('DetailViewPage', () => {
    jest.useFakeTimers();
    const tree = renderer.create(<DetailedViewPage />).toJSON();
    expect(tree).toMatchSnapshot();
});


test('HomePage', () => {
    jest.useFakeTimers();
    const tree = renderer.create(<HomePage />).toJSON();
    expect(tree).toMatchSnapshot();
});

test('SearchPage', () => {
    jest.useFakeTimers();
    const tree = renderer.create(<SearchPage />).toJSON();
    expect(tree).toMatchSnapshot();
});


