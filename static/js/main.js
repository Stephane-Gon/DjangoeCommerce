import * as helper from './helpers.js'
import * as cart from './cart.js'
import * as cookie from './cookies.js'



document.addEventListener('DOMContentLoaded', () => {
    // HERE I GIVE FUNCTIONALITY TO THE MESSAGES POP UP
    let msgWrapper = document.getElementById('messages')
    if(msgWrapper.innerText != '') {
        let icon = document.getElementById('messagesExitIcon')
        helper.messagesExit(icon, msgWrapper)
    }

    // HERE I STORE A COOKIE WITH THE USER VIEWPORT
    let userWidth = document.documentElement.clientWidth
    cookie.setCookie('viewport', userWidth, '/', 5)

    // HERE I CALL THE COOKIES CONSENT FUNCTIONS
    let cookiePrefBtn = document.getElementById('cookie-preferences-btn')
    let cookiePrefWrapper = document.getElementById('cookie-preferences-wrapper')

    cookiePrefBtn.addEventListener('click', () => {
        cookiePrefWrapper.style.display = 'block'
    })
    
    let prefExitIcon = document.getElementById('cookiePrefExitIcon')
    helper.messagesExit(prefExitIcon, cookiePrefWrapper)
    cookie.cookieConsent()

    // HERE I CALL THE BURGER MENU FUNCTION
    const menuBtn = document.querySelector('.menu-btn');
    const sideNav = document.querySelector('.side-menu-user')
    helper.burgerMenu(menuBtn, sideNav)

})

if(urlName === 'login' || urlName === 'register') {

    // FRONTEND SCRIPTS
    const signUpBtn = document.getElementById('signUp')
    const signInBtn = document.getElementById('signIn')
    const container = document.getElementById('loginContainer')

    if (document.title === 'Register Page') {
        if(document.documentElement.clientWidth < 768) {
            container.classList.add('top-panel-active')
        }
        else {
            container.classList.add('right-panel-active')
        }
    }


    signUpBtn.addEventListener('click', () => {
        if(document.documentElement.clientWidth < 768) {
            container.classList.add('top-panel-active')
        }
        else {
            container.classList.add('right-panel-active')
        }
    })

    signInBtn.addEventListener('click', () => {
        if(document.documentElement.clientWidth < 768) {
            container.classList.remove('top-panel-active')
        }
        else {
            container.classList.remove('right-panel-active')
        }
    })

    const inputs = document.querySelectorAll('input')
    helper.changeMyLabel(inputs, '#C19770', '#644936')
    let pass1Input = inputs[3]
    let pass2Input = inputs[4]
    helper.registerErrorCheck(pass1Input, pass2Input) // DESATIVEI PORQUE NÃO FÁZ NADA

}


if(urlName === 'reset_password' || urlName === 'password_reset_confirm') {
    const inputs = document.querySelectorAll('input')
    helper.changeMyLabel(inputs, '#C19770', '#644936')
}

if (urlName === 'user-account'){

    // MESSAGES AND USERNAV
    let userNav = document.getElementById('userAccountNav')
    let messagesBtn = document.getElementById('messagesExitIcon')
    helper.userProfileMessages(messagesBtn, userNav)

    // USERNAV DESIGN
    let marker = document.getElementById('marker')
    let navLinks = document.querySelectorAll('.userNavLink')
    let userWrappers = document.getElementsByClassName('profile-wrapper')
    helper.userAccount(navLinks, userWrappers, marker, 'user')

    // LABELS & INPUTS DESIGN
    const inputs = document.querySelectorAll('.myInput')
    helper.changeMyLabel(inputs, '#C19770', '#644936')

    // FUNCTION THAT REDIRECTS USER
    helper.profileRedirect(navLinks, userWrappers, marker)

    // DELETES DEFAULT PLACEHOLDER FROM INPUT
    helper.deleteDefaultInput(inputs)

    // ASYNCRHONOUS ERROR CHECKING FOR USER NAMES
    let firstNameInput = document.getElementById('first_name')
    helper.errorCheck(firstNameInput, 'first name')
    let lastNameInput = document.getElementById('last_name')
    helper.errorCheck(lastNameInput, 'last name')

    // ASYNCRHONOUS ERROR CHECKING FOR PASSWORD
    let new_password1 = document.getElementById('new_password1')
    let new_password2 = document.getElementById('new_password2')
    helper.passErrorCheck(new_password1, new_password2)
}
else {
    document.cookie = 'profileCookie=;expires=Thu, 01 Jan 2000 00:00:01 GMT'
}

if (urlName === 'home' || urlName === 'about'){
    let footerGap = document.querySelector('.footer-gap')
    footerGap.style.paddingTop = '30px'
   
}

if (urlName === 'home' || urlName === 'product'){
    let cardImgBox = document.querySelectorAll('.card-img-box')

    for(let i= 0; i < cardImgBox.length; i++) {
        let imgUrl = cardImgBox[i].dataset.img
        cardImgBox[i].style.backgroundImage = `url("${imgUrl}")`
    }
   
}

if (urlName === 'gallery') {
    let images = document.querySelectorAll('img')
    helper.sendImgUrl(images)
}

if ( urlName === 'single-categorie') {

    let updateBtns = document.getElementsByClassName('update-cart')
    cart.updateCart(updateBtns)

    // HERE I MAKE THE SIDE CATEGORIES BAR LOGIC
    let catTooltip = document.getElementById('cat-Tooltip')
    let catNavBar = document.getElementById('cat-NavBar')
    helper.categorieNavBar(catTooltip, catNavBar)
}

if (urlName === 'product') {
    let switchDesc = document.querySelector('.switch-desc')
    let switchReview = document.querySelector('.switch-reviews')
    let switchTitles = document.querySelectorAll('.switch-titles h1')
    helper.switchContainers(switchDesc, switchReview, switchTitles)

    let updateBtns = document.getElementsByClassName('update-cart')
    cart.updateCart(updateBtns)

    let modelBg = document.querySelector('.refund-modalBg')
    let modelBtn = document.getElementById('refundBtn')
    let leaveBtn = document.getElementById('model-exit-icon')
    let activeClass = 'modalBgActive'
    if( modelBtn != null) {
        helper.modelPopUp(modelBtn, modelBg, leaveBtn, activeClass)
    }
}
if (urlName === 'cart' ) {
    let updateBtns = document.getElementsByClassName('update-cart')
    cart.updateCart(updateBtns)
}

if (urlName === 'check-user' || urlName === 'checkout'){

    // MESSAGES AND USERNAV
    let checkoutNav = document.getElementById('userAccountNav')
    let messagesBtn = document.getElementById('messagesExitIcon')
    helper.userProfileMessages(messagesBtn, checkoutNav)

    // LABELS & INPUTS DESIGN
    const inputs = document.querySelectorAll('.myInput')
    helper.changeMyLabel(inputs, '#C19770', '#644936')

    // USERNAV DESIGN
    let requiredInputs = document.querySelectorAll('[required]');
    let marker = document.getElementById('marker')
    let navLinks = document.querySelectorAll('.userNavLink')
    let checkoutWrappers = document.getElementsByClassName('checkout-wrapper')

    // HERE I CALL THE "userAccount" FUNCTION ONLY IF THE USER HAS AN ADDRESS
    let counter = 0
    for (let i = 0; i < requiredInputs.length; i++) {
        if(requiredInputs[i].value === ''){
            break
        }
        else{
            counter++
        }
    }
    if(requiredInputs.length === counter) {
        helper.userAccount(navLinks, checkoutWrappers, marker, null, 'block')
    }

    // HERE I DISABLE THE RECEIPT LINK WHILE THE TRANSACTION IS NOT READY
    if (checkoutWrappers[2].dataset.status != 'completed') {
        navLinks[2].style.pointerEvents = 'none'
    }

    // DELETES DEFAULT PLACEHOLDER FROM INPUT
    helper.deleteDefaultInput(inputs)
}

if (urlName === 'order-details' ) {
    let modelBg = document.querySelector('.refund-modalBg')
    let modelBtns = document.querySelectorAll('.refundBtn')
    let leaveBtn = document.getElementById('model-exit-icon')
    let activeClass = 'modalBgActive'
    let label = document.getElementById('qty-label')
    let itemInput = document.getElementById('item-input')

    // HERE I DEAL WITH THE MODAL AND REFUND FORM LOGIC
    for(let i = 0; i < modelBtns.length; i++) {
        if( modelBtns[i] != null) {
            helper.modelPopUp(modelBtns[i], modelBg, leaveBtn, activeClass, label, itemInput)
        }
        helper.refundForm(modelBtns[i], label, itemInput)
    }

    // HERE I MAKE THE LOGIC FOR THE CANCEL FORMS
    let cancelBtns = document.querySelectorAll('.cancel-btns')
    document.addEventListener('DOMContentLoaded', () => {
        helper.cancelRefundLogic(cancelBtns)
    })

    // HERE I MAKE AN ASYNCHRONOS CHECK OF THE NUMBER OF FILES
    let refundImg = document.getElementById('refund-image')
    refundImg.addEventListener('change', () => {
        let max_images = document.getElementById('refund-quantity').value * 2
        let messages = document.getElementById('messages')

        if(refundImg.files.length > max_images) {
            // HERE I DELETE THE FILES FROM THE INPUT
            refundImg.value = ''

            // HERE I DISPLAY THE MESSAGE
	        messages.innerHTML = `<h4 class="alert-error">You can only add a maximum of ${max_images} images.</h4>
						  <i class="fas fa-times" id="messagesExitIcon" aria-hidden="true">`
	        messages.style.display = 'flex'

            let icon = document.getElementById('messagesExitIcon')
	        helper.messagesExit(icon, messages)
        }
        else if(refundImg.files.length < document.getElementById('refund-quantity').value) {
            // HERE I DELETE THE FILES FROM THE INPUT
            refundImg.value = ''

            // HERE I DISPLAY THE MESSAGE
	        messages.innerHTML = `<h4 class="alert-error">You need to send at least one image per product.</h4>
						  <i class="fas fa-times" id="messagesExitIcon" aria-hidden="true">`
	        messages.style.display = 'flex'

            let icon = document.getElementById('messagesExitIcon')
	        helper.messagesExit(icon, messages)
        }
    })

}