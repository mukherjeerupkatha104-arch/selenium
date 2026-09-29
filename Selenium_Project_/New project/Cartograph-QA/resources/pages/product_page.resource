*** Settings ***
Resource    ../locators/common.resource
Resource    ../locators/product.resource
Resource    ../keywords/framework.resource
Library     SeleniumLibrary
Library     String

*** Keywords ***
Open Product Search
    # Direct page navigation is less fragile than a header click on this public demo site,
    # whose cookie/ad overlays can intercept the navigation control.
    Go To    ${BASE_URL}products
    Wait Until Location Contains    /products    ${TIMEOUT}
    Dismiss Site Overlays
    Wait Until Element Is Visible    ${SEARCH_INPUT}    ${TIMEOUT}

Search Catalog
    [Arguments]    ${search_term}
    Dismiss Site Overlays
    Input Text    ${SEARCH_INPUT}    ${search_term}
    Js Click    ${SEARCH_SUBMIT}

Search Results Should Be Available
    Wait Until Keyword Succeeds    3x    1s    Wait Until Element Is Visible    ${SEARCHED_PRODUCTS}    ${TIMEOUT}

No Matching Products Should Be Shown
    Wait Until Page Contains    Searched Products    ${TIMEOUT}
    Page Should Not Contain Element    xpath=//div[contains(@class,'productinfo')]

Add Named Product To Cart
    [Arguments]    ${product_name}
    Wait Until Keyword Succeeds    5x    2s    Trigger Add To Cart    ${product_name}

Trigger Add To Cart
    [Arguments]    ${product_name}
    ${card}=    Replace String    ${PRODUCT_CARD}    __PRODUCT__    ${product_name}
    # Automation Exercise duplicates the cart control and can cover one copy with the
    # other. Resolve the card's stable control and trigger it through the DOM.
    ${add_button}=    Set Variable    ${card}//a[contains(@class,'add-to-cart')]
    Dismiss Site Overlays
    Scroll Element Into View    ${add_button}
    ${button_element}=    Get WebElement    ${add_button}
    Execute Javascript    arguments[0].click();    ARGUMENTS    ${button_element}
    Wait Until Page Contains Element    ${ADDED_MODAL}    8s
    Close Added To Cart Modal

Close Added To Cart Modal
    ${modal_open}=    Run Keyword And Return Status    Page Should Contain Element    ${ADDED_MODAL}
    Return From Keyword If    not ${modal_open}
    Dismiss Site Overlays
    Js Click    ${CONTINUE_SHOPPING}
    Wait Until Element Is Not Visible    ${ADDED_MODAL}    8s
