*** Settings ***
Resource    ../locators/common.resource
Resource    ../keywords/framework.resource
Library     SeleniumLibrary

*** Keywords ***
Open Login Page
    Go To    ${BASE_URL}login
    Dismiss Site Overlays
    Wait Until Element Is Visible    ${LOGIN_EMAIL}    ${TIMEOUT}

Submit Credentials
    [Arguments]    ${email}    ${password}
    Dismiss Site Overlays
    Input Text    ${LOGIN_EMAIL}    ${email}
    Input Password    ${LOGIN_PASSWORD}    ${password}
    Js Click    ${LOGIN_SUBMIT}

Login Should Be Successful
    Wait Until Keyword Succeeds    3x    2s    Wait Until Element Is Visible    ${LOGGED_IN_BANNER}    ${TIMEOUT}

Log Out
    Go To    ${BASE_URL}logout
    Dismiss Site Overlays
    Wait Until Keyword Succeeds    3x    2s    Wait Until Element Is Visible    ${NAV_LOGIN}    ${TIMEOUT}
