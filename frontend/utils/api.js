import fetch from 'node-fetch'

const BACKEND_URL = 'http://grocerybuddybackend.azurewebsites.net'

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