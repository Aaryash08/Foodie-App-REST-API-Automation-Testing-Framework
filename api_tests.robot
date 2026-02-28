*** Settings ***
Library           RequestsLibrary
Library           Collections
Library           BuiltIn
Suite Setup       Setup Suite
Suite Teardown    Teardown Suite

*** Variables ***
&{RESTAURANT_DATA}    name=Spice Garden    category=Indian    location=North    images=@{EMPTY}    contact=98765
&{DISH_DATA}          name=Paneer Tikka    type=Veg    price=15.0    available_time=All Day    image=paneer.jpg

*** Keywords ***
Setup Suite
    Create Session    foodie    http://localhost:5000/api/v1
    # Reset backend if endpoint exists (safe even if it doesn't)
    Run Keyword And Ignore Error    POST On Session    foodie    /admin/reset
    ${rand}=    Evaluate    __import__('uuid').uuid4().hex[:6]
    Set Suite Variable    ${RAND}
    &{USER_DATA}=    Create Dictionary    name=John Doe    email=john_robot_${RAND}@example.com    password=secret123
    Set Suite Variable    &{USER_DATA}

Teardown Suite
    Delete All Sessions

*** Test Cases ***

# RESTAURANT MODULE

Register New Restaurant Successfully
    ${response}=    POST On Session    foodie    /restaurants    json=${RESTAURANT_DATA}
    Status Should Be    201    ${response}
    ${json}=    Set Variable    ${response.json()}
    Set Suite Variable    ${NEW_RES_ID}    ${json['id']}

Update Restaurant Details
    ${update_data}=    Create Dictionary    location=South
    ${response}=    PUT On Session    foodie    /restaurants/${NEW_RES_ID}    json=${update_data}
    Status Should Be    200    ${response}
    Should Be Equal As Strings    ${response.json()['location']}    South

Approve Restaurant Via Admin
    ${response}=    PUT On Session    foodie    /admin/restaurants/${NEW_RES_ID}/approve
    Status Should Be    200    ${response}
    Should Be Equal As Strings    ${response.json()['message']}    Restaurant approved

# DISH MODULE

Add Dish To Restaurant
    ${response}=    POST On Session    foodie    /restaurants/${NEW_RES_ID}/dishes    json=${DISH_DATA}
    Status Should Be    201    ${response}
    Set Suite Variable    ${NEW_DISH_ID}    ${response.json()['id']}

Update Dish Status
    ${status}=    Create Dictionary    enabled=${FALSE}
    ${response}=    PUT On Session    foodie    /dishes/${NEW_DISH_ID}/status    json=${status}
    Status Should Be    200    ${response}

# USER & SEARCH MODULE

Register New User
    ${response}=    POST On Session    foodie    /users/register    json=${USER_DATA}
    Status Should Be    201    ${response}
    Set Suite Variable    ${USER_ID}    ${response.json()['id']}

Search For Restaurant By Name
    ${params}=    Create Dictionary    name=Spice    location=South
    ${response}=    GET On Session    foodie    /restaurants/search    params=${params}
    Status Should Be    200    ${response}
    Should Not Be Empty    ${response.json()}

# ORDER & RATING MODULE

Place An Order
    ${dishes_list}=    Create List    ${NEW_DISH_ID}
    ${order_payload}=    Create Dictionary    user_id=${USER_ID}    restaurant_id=${NEW_RES_ID}    dishes=${dishes_list}
    ${response}=    POST On Session    foodie    /orders    json=${order_payload}
    Status Should Be    201    ${response}
    Set Suite Variable    ${ORDER_ID}    ${response.json()['id']}

Submit Rating And Feedback
    ${rating_payload}=    Create Dictionary    order_id=${ORDER_ID}    rating=5    comment=Excellent food!
    ${response}=    POST On Session    foodie    /ratings    json=${rating_payload}
    Status Should Be    201    ${response}

View Admin Feedback
    ${response}=    GET On Session    foodie    /admin/feedback
    Status Should Be    200    ${response}
    Should Not Be Empty    ${response.json()}

# CLEAN Data

Delete Dish
    ${response}=    DELETE On Session    foodie    /dishes/${NEW_DISH_ID}
    Status Should Be    200    ${response}

Delete Restaurant
    ${response}=    DELETE On Session    foodie    /restaurants/${NEW_RES_ID}
    Status Should Be    200    ${response}