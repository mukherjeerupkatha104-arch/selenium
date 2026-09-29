*** Settings ***
Resource    ../pages/login_page.resource
Resource    ../pages/product_page.resource
Resource    ../pages/cart_page.resource
Library     Collections

*** Keywords ***
Login As Configured User
    Should Not Be Empty    ${TEST_EMAIL}    Configure AE_EMAIL in .env or the CI credential store.
    Should Not Be Empty    ${TEST_PASSWORD}    Configure AE_PASSWORD in .env or the CI credential store.
    Open Login Page
    Submit Credentials    ${TEST_EMAIL}    ${TEST_PASSWORD}
    Login Should Be Successful

Complete Product Journey From Dataset
    [Arguments]    ${case}
    ${search}=    Get From Dictionary    ${case}    search
    ${expected_result}=    Get From Dictionary    ${case}    expected_result
    Login As Configured User
    Open Product Search
    Search Catalog    ${search}
    Run Keyword If    '${expected_result}' == 'found'    Complete Successful Cart Journey    ${case}
    ...    ELSE    No Matching Products Should Be Shown
    Log Out

Complete Successful Cart Journey
    [Arguments]    ${case}
    ${product}=    Get From Dictionary    ${case}    product
    ${expected_cart}=    Get From Dictionary    ${case}    expected_cart
    Search Results Should Be Available
    Add Named Product To Cart    ${product}
    Open Cart
    Cart Should Contain Product    ${expected_cart}
