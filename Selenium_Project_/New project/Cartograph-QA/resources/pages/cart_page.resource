*** Settings ***
Resource    ../locators/common.resource
Resource    ../locators/product.resource
Resource    ../keywords/framework.resource
Library     SeleniumLibrary
Library     String

*** Keywords ***
Open Cart
    Go To    ${BASE_URL}view_cart
    Dismiss Site Overlays
    Wait Until Location Contains    /view_cart    ${TIMEOUT}

Cart Should Contain Product
    [Arguments]    ${product_name}
    ${row}=    Replace String    ${CART_ROW}    __PRODUCT__    ${product_name}
    Wait Until Keyword Succeeds    3x    2s    Wait Until Element Is Visible    ${row}    ${TIMEOUT}
