import * as helper from './helpers.js'


// THIS FUNCTION CHECKS IF THE USER IS LOGGED IN OR NOT 
// AND CALLS A DIFFERENT FUNCTION DEPENDING ON THE RESULT
export function updateCart(btns) {
	for (let i = 0; i < btns.length; i++) {
		btns[i].addEventListener('click', function(){
			var productId = this.dataset.product
			var action = this.dataset.action
	
			if (user == 'AnonymousUser'){
				addCookieItem(productId, action)
			}else{
				updateUserOrder(productId, action)
			}
		})
	}
}

// THIS FUNCTION SENDS A FETCH CALL WITH THE PRODUCT ID TO THE UPDATE_VIEW
function updateUserOrder(productId, action){
		var url = '/update/'

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
			displayValues(data)
		});
}

function displayValues(data) {

	// HERE I UPDATE THE CART ICON
	let cartItemsDisplay = document.getElementById('cartItems')
	let sideCartItemsDisplay = document.getElementById('sideCartItems')
	cartItemsDisplay.innerText = data['cartItems']
	sideCartItemsDisplay.innerText = data['cartItems']
	
	// HERE I DISPLAY THE MESSAGE
	let messages = document.getElementById('messages')
	messages.innerHTML = `<h4 class="alert-success">${data['message']}</h4>
						  <i class="fas fa-times" id="messagesExitIcon" aria-hidden="true">`
	messages.style.display = 'flex'

	let icon = document.getElementById('messagesExitIcon')
	helper.messagesExit(icon, messages)

	// HERE I CHECK IF THE USER IS IN THE CART URL, IF SO I DISPLAY THE NEW VALUES
	if(urlName === 'cart') {
		let userWidth = document.documentElement.clientWidth
		if( userWidth > 500) {
			if(data['itemQuantity'] === 0) {
					let itemRow = document.getElementById(`item-${data['itemId']}`)
					itemRow.remove()
			}
			else {
					let itemTotalDisplay = document.getElementById(`itemTotal-${data['itemId']}`)
					itemTotalDisplay.innerText = data['itemTotal'] + '€'
		
					let itemQtyDisplay = document.getElementById(`itemQuantity-${data['itemId']}`)
					itemQtyDisplay.innerText = data['itemQuantity']
			}
		}
		else{
			if (data['itemQuantity'] === 0) {
					let itemRow = document.getElementById(`item-phone-${data['itemId']}`)
					itemRow.remove()
			}
			else if (data['itemQuantity'] != 0){
					let itemTotalDisplay = document.getElementById(`item-Total-phone-${data['itemId']}`)
					itemTotalDisplay.innerText = data['itemTotal'] + '€'
		
					let itemQtyDisplay = document.getElementById(`itemQty-phone-${data['itemId']}`)
					itemQtyDisplay.innerText = data['itemQuantity']
			}
		}

		let tRows = document.querySelectorAll('.table-row')
		let phoneWrapper = document.querySelector('.phone-items-wrapper')
		if (tRows.length === 0 && userWidth > 500) {
			let table = document.querySelector('.cart-items-wrapper')
			let summary = document.querySelector('.summary-wrapper')
			table.remove()
			summary.remove()

			let cartWrapper = document.querySelector('.cart-wrapper')
			let textDiv = document.createElement('div')
			textDiv.classList.add('align-h')

			let heading = document.createElement('h1')
			heading.classList.add('mainHeading')
			heading.innerText = 'Your JoaoLina cart is empty.'

			textDiv.appendChild(heading)
			cartWrapper.appendChild(textDiv)
		}
		else if(phoneWrapper.innerText === '' && userWidth <= 500) {
				let summary = document.querySelector('.summary-wrapper')
				phoneWrapper.remove()
				summary.remove()

				let cartWrapper = document.querySelector('.cart-wrapper')
				let textDiv = document.createElement('div')
				textDiv.classList.add('align-h')

				let heading = document.createElement('h1')
				heading.classList.add('mainHeading')
				heading.innerText = 'Your JoaoLina cart is empty.'

				textDiv.appendChild(heading)
				cartWrapper.appendChild(textDiv)
		}
		else {
			let orderSubTotalHtml = document.getElementById('order-subTotal')
			let orderShippingHtml = document.getElementById('order-shipping')
			let orderTotalHtml = document.getElementById('order-total')

			orderSubTotalHtml.innerHTML = `<p id="order-subTotal"><strong>Subtotal: </strong>${data['order_subTotal']}€</p>`
			orderShippingHtml.innerHTML = `<p id="order-shipping"><strong>Shipping: </strong>${data['order_shipping']}€</p>`
			orderTotalHtml.innerHTML = `<p id="order-total"><strong>Total: </strong>${data['order_total']}€</p>`
		}
	}
}

// THIS FUNCTION CREATS THE CART FOR THE ANONYMOUS USER'S
function addCookieItem(productId, action) {
	if(action == 'add') {
		if(cart[productId] == undefined){
			cart[productId] = { 'quantity': 1 }
		} 
		else {
			cart[productId]['quantity'] += 1
		}
	}
	else if (action == 'remove') {
		cart[productId]['quantity'] -= 1
	}

	if(cart[productId]['quantity'] <= 0 || action == 'delete') {
		delete cart[productId]
	}

	let expiryDate = new Date();
	expiryDate.setTime(expiryDate.getTime() + (30 * 24 * 60 * 60 * 1000));

	document.cookie = 'cart=' + JSON.stringify(cart) + ";expires=" + expiryDate + ";domain=;path=/;SameSite=Lax"
	location.reload()
}