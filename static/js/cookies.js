// FUNCTION THAT SETA A COOKIE
export function setCookie(cName, cValue, cPath='/', expDays) {
    
    let expires
    if(expDays) {
        let date = new Date();
        date.setTime(date.getTime() + (expDays * 24 * 60 * 60 * 1000));
        expires = "expires=" + date.toUTCString();
    } 
    else {
        expires = ''
    }
    document.cookie = `${cName}=${cValue}; ${expires}; path=${cPath};SameSite=Lax`
}

// FUNCTION THAT GETS A COOKIE
export function getCookie(cName) {
    const name = cName + "=";
    const cDecoded = decodeURIComponent(document.cookie); //to be careful
    const cArr = cDecoded .split('; ');
    let res;
    cArr.forEach(val => {
        if (val.indexOf(name) === 0) res = val.substring(name.length);
    })
    return res;
}


// FUNCTION THAT DEALS WITH THE COOKIE CONSENT
export function cookieConsent() {
    const cookieStorage = {
        getItem: (item) => {
            const cookies = document.cookie
                .split(';')
                .map(cookie => cookie.split('='))
                .reduce((acc, [key, value]) => ({ ...acc, [key.trim()]: value }), {});
            return cookies[item];
        },
        setItem: (item, value) => {
            setCookie(item, value, '/', 365)
        }
    }
    
    const storageType = cookieStorage;
    const consentPropertyName = 'jdc_consent';
    const shouldShowPopup = () => !storageType.getItem(consentPropertyName);
    const saveToStorage = () => storageType.setItem(consentPropertyName, true);
    
    window.onload = () => {
        const acceptFn = event => {
            saveToStorage(storageType);
            consentPopup.classList.add('consent-hidden');
        }
        const consentPopup = document.getElementById('consent-popup');
        const acceptBtn = document.getElementById('accept');
        acceptBtn.addEventListener('click', acceptFn);
    
        if (shouldShowPopup(storageType)) {
            setTimeout(() => {
                consentPopup.classList.remove('consent-hidden');
            }, 2000);
        }
    
    };
}