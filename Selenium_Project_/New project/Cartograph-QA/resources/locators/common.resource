*** Variables ***
${NAV_LOGIN}             xpath=//a[contains(normalize-space(.), 'Signup / Login')]
${NAV_PRODUCTS}          xpath=//a[@href='/products']
${NAV_CART}              xpath=//a[@href='/view_cart']
${NAV_LOGOUT}            xpath=//a[@href='/logout']
${LOGGED_IN_BANNER}      xpath=//a[contains(normalize-space(.), 'Logged in as')]
${LOGIN_EMAIL}           css=input[data-qa='login-email']
${LOGIN_PASSWORD}        css=input[data-qa='login-password']
${LOGIN_SUBMIT}          css=button[data-qa='login-button']
${SEARCH_INPUT}          css=input#search_product
${SEARCH_SUBMIT}         css=button#submit_search
${SEARCHED_PRODUCTS}     xpath=//h2[normalize-space()='Searched Products']
${NO_PRODUCT_MESSAGE}    xpath=//p[contains(normalize-space(.), 'No products')]
${ADDED_MODAL}           css=#cartModal
${CONTINUE_SHOPPING}     xpath=//button[normalize-space()='Continue Shopping']
