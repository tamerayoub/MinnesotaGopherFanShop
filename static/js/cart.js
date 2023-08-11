// Modified by Tamer Ayoub - 08/11/2023


// This file handles logic when updating product quantity from the cart.html and store.html template


// This line selects all elements with the class name update-cart in the cart and store template
var updateBtns = document.getElementsByClassName('update-cart')

// This loop iterates over each element with the class 'update-cart'
for (i = 0; i < updateBtns.length; i++) {

	// when a user clicks on one of the update-cart elements - event listern
	updateBtns[i].addEventListener('click', function(){

		// collects productid and add or remove action from the element that was clicked
		var productId = this.dataset.product
		var action = this.dataset.action
		
		// display our results
		console.log('productId:', productId, 'Action:', action)
		console.log('USER:', user)

		// if user is anonymous, call addCookieItem to update the cart, otherwise call updateUserOrder
		if (user == 'AnonymousUser'){
			addCookieItem(productId, action)
		}else{
			updateUserOrder(productId, action)
		}
	})
}


// if user isnt anonymous, call updateUserOrder when updating the cart
function updateUserOrder(productId, action){
	console.log('User is authenticated, sending data...')

	// a url to the view UpdateItem
	var url = '/update_item/'

	// fetch the url update-item and post the data productId and action
	fetch(url, {
		method:'POST',
		headers:{
			'Content-Type':'application/json',
			'X-CSRFToken':csrftoken,
		}, 
		body:JSON.stringify({'productId':productId, 'action':action})
	})
	.then((response) => {
		return response.json();
	})
	.then((data) => {
		location.reload()
	});
}


// if user is anonymous, call addCookieItem when updating the cart
function addCookieItem(productId, action){
	console.log('User is not authenticated')

	if (action == 'add'){

		// if product doesnt exist in the cart, create a new entry w/ a quantity of 1
		if (cart[productId] == undefined){
		cart[productId] = {'quantity':1}

		// if product doesnt exist in the cart, create a new entry w/ a quantity of 1
		}else{
			cart[productId]['quantity'] += 1
		}
	}

	if (action == 'remove'){
		// given the productId, remove the quantity by 1
		cart[productId]['quantity'] -= 1
		
		// if the quantity is 0 or less, delete the product
		if (cart[productId]['quantity'] <= 0){
			console.log('Item should be deleted')
			delete cart[productId];
		}
	}

	
	console.log('CART:', cart)

	// This line is responsible for updating the browser's cookies with the contents of the cart object,
	// effectively storing the cart data in a cookie named 'cart'. 
	document.cookie ='cart=' + JSON.stringify(cart) + ";domain=;path=/"
	
	// This line reloads the current page, effectively refreshing the page
	location.reload()
}