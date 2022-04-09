import * as cookies from './cookies.js'

// ORDER DETAILS REFUND FORM FUNCTION
export function refundForm(modelBtn, label, itemInput) {

    modelBtn.addEventListener('click', () => {
        let itemQuantity = parseInt(modelBtn.dataset.qty)
        let itemId = modelBtn.dataset.item
        
        label.innerText = `Refund from 0 to ${itemQuantity} of this item.`
        itemInput.value = itemId
    })
}

// FUNCTION THAT DEALS WITH THE CANCEL REFUND LOGIC
export function cancelRefundLogic( btns){
    let cancelItems = document.querySelectorAll('.cancel-form')
    
    for(let i = 0; i < cancelItems.length; i++ ) {
        let itemId = btns[i].dataset.item // I GET THE ITEM ID

        // I CREATE THE HIDDEN INPUT
        let hiddenInput = document.createElement('input')
        hiddenInput.type = "hidden"
        hiddenInput.setAttribute('name', 'item')
        hiddenInput.setAttribute('id', itemId)
        hiddenInput.classList.add('cancel-item-input')
        hiddenInput.value = itemId
        
        // IN CREATE THE LABEL
        let label = document.createElement('label')
        label.classList.add('myCheckbox')

        // I CREATE THE CHECKBOX INPUT
        let cancelInput = document.createElement('input')
        cancelInput.classList.add('hidden-checkbox')
        cancelInput.type = 'checkbox'
        cancelInput.setAttribute("name","cancel")
        cancelInput.setAttribute("required","")

        let div = document.createElement('div')
        div.classList.add('checkbox-box')

        let b = document.createElement('b')
        b.innerText = 'Check to cancel refund'
 
        // I APPEND THE LAST 3 ELEMENTS TO THE LABEL
        label.appendChild(cancelInput)
        label.appendChild(div)
        label.appendChild(b)

        let csrf_token = cancelItems[i].firstElementChild
        
        // I APPEND THE HIDDEN INPUT AFTER THE CSRF_TOKEN
        csrf_token.parentNode.insertBefore(hiddenInput, csrf_token.nextSibling)

        // I APPEND THE LABEL AFTER THE HIDDEN INPUT
        hiddenInput.parentElement.insertBefore(label, hiddenInput.nextSibling)

    }
}

// BURGER MENU FUNCTION
export function burgerMenu(menuBtn, sideNav) {
    let menuOpen = false
    menuBtn.addEventListener('click', () => {
        if(!menuOpen) {
          menuBtn.classList.add('open');
          menuOpen = true;
          sideNav.classList.add('side-nav-open')
        } else {
          menuBtn.classList.remove('open');
          menuOpen = false;
          sideNav.classList.remove('side-nav-open');
        }  
    })
    let innerBtn = document.querySelector('.menu-btn__burger')
    window.onclick = function(event) {
		if (event.target != menuBtn && event.target != sideNav && event.target != innerBtn && menuOpen == true) {
            menuBtn.classList.remove('open');
            menuOpen = false;
            sideNav.classList.remove('side-nav-open'); 
		}
	}
}

// CATEGORIES NAVBAR FOR PHONE FUNCTION
export function categorieNavBar(tooltip, navbar) {
    let navBarFChild = navbar.firstElementChild

    tooltip.addEventListener('click', () => {

        // HERE I CHANGE THE TOOLTIP HTML
        tooltip.style.display = 'none'

        // NAVBAR STYLING
        navbar.style.display = 'block'
        navbar.style.position = 'fixed'
        navbar.style.opacity = 1
    })
    navBarFChild.addEventListener('click', () => {
        navbar.style.display = 'none'
        tooltip.style.display = 'block'
    })
}

// MODEL POP UP FUNCTION
export function modelPopUp(showBtn, modelBg, leaveBtn, activeClass, label, itemInput) {

	modelBg.style.overflowY = 'auto';
		
    showBtn.addEventListener('click', () => {
        modelBg.classList.add(activeClass)
		document.body.style.overflow = 'hidden'
    })
    leaveBtn.addEventListener('click', ()=> {
        modelBg.classList.remove(activeClass)
		document.body.style.overflow = 'scroll'
        label.innerText = ''
        itemInput.value = ''
    })
    modelBg.addEventListener('click', (event) => {
        if (event.target == modelBg) {
            modelBg.classList.remove(activeClass)
		    document.body.style.overflow = 'scroll'
            label.innerText = ''
            itemInput.value = ''
        }
    })
}

// ESTA FUNÇÃO SERVE PARA TORNAR OS LABELS DINÁMICOS
export function changeMyLabel(inputs, color1, color2) {
    for(let i = 0; i < inputs.length; i++) {
        
        // CHECKS IF THE FORM HAS ANY ERRORS
        if(inputs[i].previousElementSibling != null && inputs[i].previousElementSibling.hasAttribute('itserror')){
            inputs[i].previousElementSibling.style.color = 'red'
        }

        // FOCUS EVENTS
        inputs[i].addEventListener('focusin', () => {
            inputs[i].previousElementSibling.style.color = color1
            inputs[i].previousElementSibling.style.transform = 'scale(0.8)'
            inputs[i].classList.add('input-active')
        })

        inputs[i].addEventListener('focusout', () => {
            if(inputs[i].value != "") {
                inputs[i].previousElementSibling.style.color = color1
                inputs[i].previousElementSibling.style.transform = 'scale(0.8)'
            } else {
                inputs[i].previousElementSibling.style.color = color2
                inputs[i].previousElementSibling.style.transform = 'scale(1)'
                inputs[i].classList.remove('input-active')
            }
            if(inputs[i].previousElementSibling.hasAttribute('itserror')) {
                inputs[i].previousElementSibling.style.color = 'red'
            }
        })

        // MOUSE EVENTS
        inputs[i].addEventListener('mouseover', () => {
            inputs[i].previousElementSibling.style.color = color1
        })

        inputs[i].addEventListener('mouseout', () => {
            if(inputs[i].classList.contains('input-active')) {
                inputs[i].previousElementSibling.style.color = color1
            } else {
                inputs[i].previousElementSibling.style.color = color2
            }
            if(inputs[i].previousElementSibling.hasAttribute('itserror')) {
                inputs[i].previousElementSibling.style.color = 'red'
            }
        })
    }
}

// FUNCTION TO CLOSE THE MESSAGES
export function messagesExit(wrapper){
    window.addEventListener('click', (event) => {
        if (event.target != wrapper && event.target != wrapper.firstElementChild) wrapper.style.display = 'None'
    })
}

// FUNCTION THAT CLOSES CONSENT POP UP
export function closeCookieConsent(icon, wrapper) {
    icon.addEventListener('click', () => {
        wrapper.style.display = 'none'
    })
}

// FUNCTION TO ANIMATE USER PROFILE PAGE NAVBAR AND TO SWITCH WRAPPERS
export function userAccount(links, wrappers, marker, pag=null, display='flex') {

    // FUNCTION TO MOVE AN ELEMENT TO A DETERMINATED PLACE
    function indicator(e) {
        // HERE I DO THIS IF STATEMENT IN CASE THE USER TRANSLATES THE PAGE
        if(e.nodeName === 'FONT') return marker.style.left = e.parentNode.parentNode.offsetLeft + 'px'
        console.log('Helo')
        return marker.style.left = e.offsetLeft + 'px'
    }

    for (let i=0; i < links.length; i++) {

        links[i].addEventListener('click', (e) => {
            
            indicator(e.target)

            for(let j=0; j < links.length; j ++) {

                if( links[j].classList.contains('active-link')) {
                    links[j].classList.remove('active-link')
                    wrappers[j].style.display = 'none'
                    
                }
            }
            links[i].classList.add('active-link')

            if(wrappers[i].classList.contains('checkout-bil-wrapper')){
                wrappers[i].style.display = 'flex'
            }
            else {
                wrappers[i].style.display = display
            }
            document.title = links[i].innerText

            if(pag == 'user') {
                cookies.setCookie('profileCookie', links[i].id);
            }
        
        })
    }


}

// FUNCTION THAT REDIRECTS USER
export function profileRedirect(links, wrappers, marker) {
    window.addEventListener('load', () => {
        let profileCookie = cookies.getCookie('profileCookie')
        if (profileCookie === undefined || profileCookie === null) return

        let link
        if(profileCookie === 'userInfoLink'){
            link = 0
        }
        else if (profileCookie === 'ordersInfoLink'){
            link = 1
        }
        else if (profileCookie === 'updateInfoLink') {
            link = 2
        }

        marker.style.left = links[link].offsetLeft + 'px'

        for (let j = 0; j < links.length; j++) {

            if (links[j].classList.contains('active-link')) {
                links[j].classList.remove('active-link')
                wrappers[j].style.display = 'none'
            }
        }

        links[link].classList.add('active-link')
        wrappers[link].style.display = 'flex'
    })
}

// FUNCTION THAT TAKES CARE OF THE MESSAGES AND USERNAV DESIGN;
export function userProfileMessages(btn, nav){    
    if(btn != null) {
        nav.style.marginTop = '50px'
        btn.addEventListener('click', () => {
            nav.style.marginTop = '10px'
        })
    }
}

// FUNCTION THAT DELETES THE INPUTS DEFAULT INFO
export function deleteDefaultInput(inputs){

    for(let i= 0; i < inputs.length; i++) {

        let tempValue = inputs[i].value

        inputs[i].addEventListener('click', () => {
            
            if (inputs[i].value = tempValue){
                inputs[i].value = ''
            }
        }, {once : true})

        inputs[i].addEventListener('blur', () => {

            if (inputs[i].value === '') { 
                inputs[i].value = tempValue
            }
        }, {once : true})
    }
}

// FUNCTION THAT MAKES THE ERROR CHECKING IN THE FRONTEND ASYNCHRONOUS
export function errorCheck(input, field) {
    let formatedField = field.replace(" ", "_")

    input.addEventListener('input', () => {

        let newValue = input.value
        let checkErrors = document.querySelector(`.${formatedField}_errors`)
        let formatSpecialChars = /[ `!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?~]/;
        let formatNumbers = /\d/
        
        if(checkErrors == null) {
            if(formatNumbers.test(newValue) === true) {

                let errorMessageWrapper = document.createElement('div')
                errorMessageWrapper.classList.add('errorMessageWrapper', `${formatedField}_errors`)
    
                let errorMessage = document.createElement('span')
                errorMessage.classList.add('errorMessage')
    
                let errorText = document.createTextNode(`- Your ${field} can't contain numbers`)
                errorMessage.appendChild(errorText)
    
                errorMessageWrapper.appendChild(errorMessage)
    
                let formGroup = document.getElementById(`${formatedField}_group`)
                formGroup.appendChild(errorMessageWrapper)
            } 
            else if (formatSpecialChars.test(newValue) === true) {
                let errorMessageWrapper = document.createElement('div')
                errorMessageWrapper.classList.add('errorMessageWrapper', `${formatedField}_errors`)
    
                let errorMessage = document.createElement('span')
                errorMessage.classList.add('errorMessage')
    
                let errorText = document.createTextNode(`- Your ${field} can't contain special characters.`)
                errorMessage.appendChild(errorText)
    
                errorMessageWrapper.appendChild(errorMessage)
    
                let formGroup = document.getElementById(`${formatedField}_group`)
                formGroup.appendChild(errorMessageWrapper)
            }
        }
        else {
            
            if (formatSpecialChars.test(newValue) === false && formatNumbers.test(newValue) === false) {
                checkErrors.remove()
            }
            else if(formatSpecialChars.test(newValue) === true && formatNumbers.test(newValue) === true) {
                let errorText = checkErrors.firstChild
                errorText.innerText = `- Your ${field} can't contain special characters or numbers.`
            }
        }
    })

}
// FUNCTION THAT MAKES THE ERROR CHECKING IN THE FRONTEND ASYNCHRONOUS FOR THE PASSWORD
export function passErrorCheck(newPass, confirmPass) {
    
    let newPassValue
    let confirmPassValue 

    let pass1ErrorContainer = document.querySelector(`.new_pass_errors`)
    let pass2ErrorContainer = document.querySelector('.confirm_pass_errors')

    let formatUpperLetter = /[A-Z]/
    let formatNumbers = /\d/

    newPass.addEventListener('input', () => {
        newPassValue = newPass.value
        let numberError = document.querySelector('.newPassNumberError')
        let uppercaseError = document.querySelector('.newPassLetterError')
        let lenghtError = document.querySelector('.newPassLengthError')
        
        if(numberError == null && formatNumbers.test(newPassValue) === false) {

            let errorMessage = document.createElement('span')
            errorMessage.classList.add('errorMessage', 'newPassNumberError')

            let errorText = document.createTextNode(`- Your new password must contain at least 1 number.`)
            errorMessage.appendChild(errorText)

            pass1ErrorContainer.appendChild(errorMessage)
        }
        else if(numberError != null && formatNumbers.test(newPassValue) === false) {
            return
        }
        else if(numberError != null && formatNumbers.test(newPassValue) === true) {
            numberError.remove()
        }

        if(uppercaseError == null && formatUpperLetter.test(newPassValue) === false) {

            let errorMessage = document.createElement('span')
            errorMessage.classList.add('errorMessage', 'newPassLetterError')

            let errorText = document.createTextNode(`- Your new password must contain at least 1 uppercase letter.`)
            errorMessage.appendChild(errorText)

            pass1ErrorContainer.appendChild(errorMessage)
        }
        else if(uppercaseError != null && formatUpperLetter.test(newPassValue) === false) {
            return
        }
        else if(uppercaseError != null && formatUpperLetter.test(newPassValue) === true) {
            uppercaseError.remove()
        }

        if(lenghtError == null && newPassValue.length < 8) {

            let errorMessage = document.createElement('span')
            errorMessage.classList.add('errorMessage', 'newPassLengthError')

            let errorText = document.createTextNode(`- Your new password must be at least 8 characters long.`)
            errorMessage.appendChild(errorText)

            pass1ErrorContainer.appendChild(errorMessage)
        }
        else if(lenghtError != null && newPassValue.length < 8) {
            return
        }
        else if(lenghtError != null && newPassValue.length >= 8) {
            lenghtError.remove()
        }
        

    })

    confirmPass.addEventListener('input', () => {
        confirmPassValue = confirmPass.value

        if(pass2ErrorContainer == null && confirmPassValue != newPassValue) {

            pass2ErrorContainer = document.createElement('div')
            pass2ErrorContainer.classList.add('errorMessageWrapper', 'confirm_pass_errors')

            let errorMessage = document.createElement('span')
            errorMessage.classList.add('errorMessage')

            let errorText = document.createTextNode(`- Your password's don't match.`)
            errorMessage.appendChild(errorText)

            pass2ErrorContainer.appendChild(errorMessage)

            let formGroup = document.getElementById("confirm_pass_group")
            formGroup.appendChild(pass2ErrorContainer)
        }
        else if(pass2ErrorContainer != null && confirmPassValue != newPassValue) {
            return
        }
        else if(confirmPassValue === newPassValue) {
            pass2ErrorContainer.remove()
            pass2ErrorContainer = null
        }
    })
}

// FUNCTION THAT CHECKS THE REGISTER PASSWORD INPUTS
export function registerErrorCheck(pass1, pass2) {

    let formatUpperLetter = /[A-Z]/
    let formatNumbers = /\d/

    let pass1Value
    let pass2Value

    pass1.addEventListener('change', () => {
        pass1Value = pass1.value
        
        if(formatNumbers.test(pass1Value) === false || formatUpperLetter.test(pass1Value) === false || pass1Value.length < 8) {
            pass1.nextElementSibling.classList.add('inputRullerError')
        }
        else {
            pass1.nextElementSibling.classList.remove('inputRullerError')
        }
        

    })

    pass2.addEventListener('change', () => {
        pass2Value = pass2.value

        if(pass2Value != pass1Value) {
            pass2.nextElementSibling.classList.add('inputRullerError')
        }
        else {
            pass2.nextElementSibling.classList.remove('inputRullerError')
        }
    })
}


// FUNCTION THAT SEND THE IMAGE NAME TO ANOTHER VIEW;
export function sendImgUrl(images) {
    for(let i = 0; i < images.length; i++) {
        images[i].addEventListener('click', () => {
            let imgFullUrl = images[i].src

            let imgUrl = imgFullUrl.replace('https://bucket-joao-lina.s3.amazonaws.com/media/', '')
            imgUrl = imgUrl.replace('.jpg', '')
            
            location.href=`slide/${imgUrl}`
        })
    }
}


// FUNCTION TO SWITCH PRODUCT WRAPERS
export function switchContainers(wrapper1, wrapper2, titulos) {

    titulos[0].addEventListener('click', () => {
        wrapper2.style.display = 'none'
        wrapper1.style.display = 'block'
        titulos[0].style.opacity = 1
        titulos[1].style.opacity = 0.6
    })
    titulos[1].addEventListener('click', () => {
        wrapper1.style.display = 'none'
        wrapper2.style.display = 'block'
        titulos[1].style.opacity = 1
        titulos[0].style.opacity = 0.6
    })
}

