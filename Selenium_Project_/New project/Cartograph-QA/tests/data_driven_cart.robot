*** Settings ***
Documentation       Data-driven e-commerce journeys. Each test consumes an external JSON case through DataProvider.
Variables           ../libraries/ConfigProvider.py
Variables           ../libraries/DataProvider.py
Resource            ../resources/keywords/framework.resource
Resource            ../resources/keywords/business_flows.resource
Test Setup          Start Web Session
Test Teardown       Finish Test Journey
Test Template       Complete Product Journey From Dataset
Test Tags           regression    data-driven    ecommerce    login

*** Test Cases ***
Blue Top purchase journey
    [Tags]    smoke    cart    critical
    ${PRODUCT_CASES}[blue_top]

Men Tshirt purchase journey
    [Tags]    cart
    ${PRODUCT_CASES}[men_tshirt]

Unknown product search behavior
    [Tags]    search    negative
    ${PRODUCT_CASES}[unknown_product]
