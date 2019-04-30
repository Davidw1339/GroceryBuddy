import fetch from 'node-fetch';
import { AsyncStorage } from 'react-native';

const BACKEND_URL = 'https://grocerybuddybackend.azurewebsites.net';

/**
 * Takes in form data from component and casts values to match intended request
 * @param formData
 * @returns {{image: *,
 * price: number,
 * name: *,
 * upc: (*|string),
 * store: (*|string|((typedArray: int,
 * index: number, value: number) => number)|boolean|null),
 * user: *,
 * lat: number,
 * long: number}}
 */
const formatGroceryItemAdd = formData => ({
  name: formData.name,
  upc: formData.upc,
  price: parseFloat(formData.price),
  user: formData.user,
  store: formData.store,
  lat: parseFloat(formData.lat),
  long: parseFloat(formData.long),
  image: formData.image,
});

/**
 * Method that posts data to the backend
 * @param body string body of request
 * @param route RESTFul route appended to base url
 * @returns {Promise<any | never>}
 */
const postToAPI = (body, route) => fetch(BACKEND_URL + route, {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body,
}).then(resp => resp.json()).catch(error => error);

/**
 * Takes in form data from component and adds price to db
 * @param formData
 */
export const addPrice = (formData) => {
  const ROUTE = '/price';
  postToAPI(JSON.stringify(formData), ROUTE);
};


/**
 * Body: {"name", "upc", "price", "user", "store", "lat", "long"}
 Response:
 - {"success": true or false},
 - {"error": error description}
 * @param formData
 */
export const addGroceryItem = (formData) => {
  const ROUTE = '/item';
  return postToAPI(JSON.stringify(formatGroceryItemAdd(formData)), ROUTE);
};

/**
 * Returns the nearest stores given lat, long, and mile range
 * @param {current latitude} latitude
 * @param {current longitude} longitude
 * @param {range} miles
 */
export const getNearestStores = (latitude, longitude, miles) => {
  const ROUTE = `/search_gps?lat=${latitude.toString()}&long=${longitude.toString()}&miles=${miles.toString()}`;
  return fetch(BACKEND_URL + ROUTE, {
    method: 'GET',
  })
    .then(res => res.json())
    .catch(error => error);
};

/**
 * Search for an item with a keyword
 * @param {string} keyword
 */
export const searchForItem = (keyword) => {
  const LIMIT = 20;
  const ROUTE = `/search?keyword=${keyword}&limit=${LIMIT}`;
  return fetch(BACKEND_URL + ROUTE, {
    method: 'GET',
  })
    .then(res => res.json())
    .catch(error => error);
};

/**
 * Search for an item with upc code
 * @param {string} upc
 */
export const searchByUPC = (upc) => {
  const ROUTE = `${BACKEND_URL}/search?upc=${upc}`;
  return fetch(ROUTE, { method: 'GET' }).then(res => res.json());
};


/**
 * Returns all grocery lists associated with current user
 * @returns {Promise<T | Array> | *}
 */
export const getLists = () => AsyncStorage.getItem('Lists')
  .then((result) => {
    if (result === null) {
      return [{ name: 'BBQ' }];
    }
    return JSON.parse(result);
  })
  .catch(() => []);

/**
 * Adds list to local storage
 * @param currentLists
 * @param listName
 * @returns {Promise<T | never> | *}
 */
export const addList = (currentLists, listName) => {
  const newList = [
    ...currentLists,
    {
      name: listName,
      items: [],
    },
  ];
  return AsyncStorage.setItem('Lists', JSON.stringify(newList))
    .catch(error => error);
};

export const deleteList = (currentLists, listId) => {
  currentLists.splice(listId, 1);
  return AsyncStorage.setItem('Lists', JSON.stringify(currentLists))
    .catch(error => error);
};

/**
 *  sends POST request to vote for an item
 * @param voteDirection whether upvoting or downvoting
 * @param user  User initiating action
 * @param upc   UPC code of item being changed
 * @param storeObj  Store
 * @returns {Promise<any | never>}
 */
export const votePrice = (voteDirection, user, upc, storeObj) => {
  const ROUTE = '/vote';
  return fetch(BACKEND_URL + ROUTE, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      upc,
      store: storeObj.name,
      lat: storeObj.lat,
      long: storeObj.long,
      user,
      dir: voteDirection,
    }),
  })
    .then(response => response.json())
    .catch(error => error);
};

/**
 * Fetches userId from local storage
 * @returns {Promise<T | string> | *}
 */
export const getUserId = () => AsyncStorage.getItem('UserId')
  .then((result) => {
    if (result === null) {
      let userid = '';
      const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';

      for (let i = 0; i < 20; i += 1) {
        userid += possible.charAt(Math.floor(Math.random() * possible.length));
      }
      AsyncStorage.setItem('UserId', userid)
        .then(() => userid)
        .catch(error => error);
      return userid;
    }
    return result;
  })
  .catch(() => 'admin');
