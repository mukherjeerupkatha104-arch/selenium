*** Settings ***
Library     SeleniumLibrary
Library     OperatingSystem
Library     ../../libraries/BrowserFactory.py

*** Keywords ***
Start Web Session
    Run Keyword And Ignore Error    Close All Browsers
    ${options}=    Get Browser Options    ${BROWSER}    ${HEADLESS}
    Wait Until Keyword Succeeds    3x    2s    Open Browser    ${BASE_URL}    ${BROWSER}    options=${options}
    Run Keyword If    '${HEADLESS}'.lower() != 'true'    Maximize Browser Window
    Set Selenium Timeout    ${TIMEOUT}
    Set Screenshot Directory    ${OUTPUT DIR}${/}screenshots
    Dismiss Site Overlays
    Log    Execution metadata | browser=${BROWSER} | environment=${ENVIRONMENT} | build=${BUILD_ID} | headless=${HEADLESS}

Dismiss Site Overlays
    [Documentation]    Remove Google ad iframes and consent layers that intercept Selenium clicks on headed Chrome.
    Execute Javascript
    ...    document.querySelectorAll('iframe[id*="aswift"], iframe[id*="google_ads"], iframe[src*="googlesyndication"], iframe[src*="doubleclick"], iframe[name*="aswift"], iframe[id*="google_esf"], ins.adsbygoogle, div[id^="aswift"], div[id^="google_ads"], #ad_position_box, #dismiss-button, .fc-consent-root').forEach(function(el){el.remove();});

Js Click
    [Arguments]    ${locator}
    Dismiss Site Overlays
    Wait Until Page Contains Element    ${locator}    ${TIMEOUT}
    Scroll Element Into View    ${locator}
    ${element}=    Get WebElement    ${locator}
    Execute Javascript    arguments[0].click();    ARGUMENTS    ${element}

Capture Failure Evidence
    ${status}=    Run Keyword And Return Status    Should Be Equal    ${TEST STATUS}    FAIL
    Run Keyword If    ${status} and '${SCREENSHOT_ON_FAILURE}'.lower() == 'true'    Run Keyword And Ignore Error    Capture Page Screenshot    failure-{index}.png
    Run Keyword If    ${status}    Log    Business journey failed in: ${TEST NAME}. Screenshot and native Robot log are available in the result directory.    WARN

Finish Web Session
    Run Keyword And Ignore Error    Close All Browsers

Finish Test Journey
    Capture Failure Evidence
    Finish Web Session
