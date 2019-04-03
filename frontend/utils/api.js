import fetch from 'node-fetch';
import { AsyncStorage } from 'react-native';

const BACKEND_URL = 'http://grocerybuddy.eastus.cloudapp.azure.com'

/*
Takes in form data from component and casts values to match intended request
*/
const formatGroceryItemAdd = (formData) => {
    return {
        "name": formData.name,
        "upc": formData.upc,
        "price": parseFloat(formData.price),
        "user": formData.user,
        "store": formData.store,
        "lat": parseFloat(formData.lat),
        "long": parseFloat(formData.long)
    }
}

/*
Body: {"name", "upc", "price", "user", "store", "lat", "long"}
Response:
    - {"success": true or false},
    - {"error": error description}
*/
export const addGroceryItem = (formData) => {
    const ROUTE = '/item';
    console.log("we are submitting");
    return fetch(BACKEND_URL + ROUTE, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify(formatGroceryItemAdd(formData))
    })
    .then(response => response.json())
    .then(json => {
        console.log(json);
    })
    .catch((error) => {
        console.log(error);
    })
}

export const searchForItem = (keyword) => {
    const ROUTE = '/search?keyword=' + keyword
    console.log('we are searching ' + (BACKEND_URL + ROUTE));
    return fetch(BACKEND_URL + ROUTE, {
        method: "GET"
    })
    .then(res => res.json())
    .catch(error => console.error(error));
}

export const searchByUPC = (upc) => {
    const ROUTE = `${BACKEND_URL}/search?upc=${upc}`;
    return fetch(ROUTE, {method:"GET"}).then(res=>res.json());
};


/*
 * Returns all grocery lists associated with current user
 */
export const getLists = () => {
    return AsyncStorage.getItem('Lists')
    .then((result) => {
        if (result === null) {
            return [{name: "BBQ"}];
        }
        return JSON.parse(result);
    })
    .catch((error) => {
        console.log("ERROR RETRIEVING LISTS: " + error);
        return [];
    })
}

export const addList = (currentLists, listName) => {
    const newList = [
        ...currentLists,
        {
            name: listName,
            items: []
        }
    ]
    return AsyncStorage.setItem('Lists', JSON.stringify(newList))
    .catch((error) => {
        console.log("ERROR ADDING NEW LIST: " + error);
    })
}

export const deleteList = (currentLists, listId) => {
    currentLists.splice(listId, 1)
    return AsyncStorage.setItem('Lists', JSON.stringify(currentLists))
    .catch((error) => {
        console.log("ERROR DELETING LIST: " + error);
    })
}

export const votePrice = (voteDirection, user, upc, storeObj) => {
    const ROUTE = '/vote';
    return fetch(BACKEND_URL + ROUTE, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({
          upc,
          store: storeObj.name,
          lat: storeObj.lat,
          long: storeObj.long,
          user: user,
          dir: voteDirection
      })
    })
    .then(response => response.json())
    .then(json => {
        console.log(json);
    })
    .catch((error) => {
        console.log(error);
    })
} 