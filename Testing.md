# Testing Document of the Budget Calculator

- Check the Console during the testing

## Manual tests

The test are written based on the user stories and expect working functionality.

### Functional tests

#### Responsive

- Scenario: The application is working well on every resolution
    - I open the application in a browser on a <my_device>
    - I can use the application on the given resolution
    
|my_device|
|:--------:|
|PC|
|iPad|
|Mobile device|

- Scenario: Table headers and icons looks different on different resolution
    - I open the application in a browser on a <my_device>
    - On the table in the modification columns I <table_header> see the header name
    - In the table in the modification section the modification buttons contains <table_icon>

|my_device|table_header|table_icon|
|:---------:|:---------:|:---------:|
|PC|can not|Icons and full name|
|Mobile device|can|icons|

#### Alert messages

- Scenario: Every time I do modification I get back a toast message
    - I <do_action> a group or item
    - I get back toast message

|do_action|
|:----:|
|create|
|edit|
|delete|

#### Order dates

- Scenario: We can see our dates order by descending
    - I arrive on the <actual_site> page
    - I can see the given dates order by descending

|actual_site|
|:---------:|
|Dashboard|
|View details|
|Search|

#### UI/UX

- Scenario: I can see the favicon on every pages
    - I open the application
    - I check the <test_page> page
    - I can see the favicon on the browser tab

|test_page|
:-----:|
|Log in|
|Sign out|
|Dashboard|
|View details|
|Search result|

- Scenario: The pop ups has different color
    - I open and log into the application
    - I click on <test_button> button the into tha application
    - The color of the pop up is <popup_color>
    
|test_button|popup_color|
|:---------:|:---------:|
|add group|green|
|edit group|yellow|
|delete group|red|
|add sub group item|green|
|edit sub group item|yellow|
|remove sub group item|red|  
    
- Scenario: Given currency is available on every page
    - I am on the <test_page>
    - I can see the given currency next to each number

|test_page|
:-----:|
|Dashboard|
|View details|
|Search result|

- Scenario: Color of the numbers are differs
    - I am on the <test_page>
    - The negative numbers has red color and the positive numbers have red colors    

|test_page|
:-----:|
|Dashboard|
|View details|
|Search result|
    
#### Database

- Scenario: I can reach my data from database
    - I open and log into the application
    - I add a new group or item into my account
    - I can see the given data later on

#### Security

- Scenario: The url is not contains the user's name
    - I open and log into the application
    - I check the available pages
    - My name is not available from the url.

- Scenario: The user is logged out when the browser is closed
    - I open and log into the application
    - I closed the browser
    - I open the application again
    - I have to log in again

#### Sign up

- Scenario: I can sign up
    - I am on the sign up page
    - I give my details
    - I click on the sign up button
    - I redirect to the home page
    
- Scenario: After the sign up there is a Javascript message box
    - I am on the sign up page
    - I give my details
    - I click on the sign up button
    - I get back message box about the redirection

- Scenario: Passwords are not matching 
    - I am on the sign up page
    - I give my details
    - The password and password again field is not matching
    - I click on the sign up button 
    - I get back toast message about the incorrect matching

- Scenario: I get back toast message when the username is not unique
    - I am on the sign up page
    - I give my details
    - I use a not unique username
    - I click on the sign up button
    - I get back toast message about the uniqueness
    
- Scenario: The username should be more than 4 and less than9 character
    - I am on the sign up page
    - I give my details
    - I click on the Sign up page

- Scenario: I left the fields empty

- Scenario: I can choose from the currency
    - I am on the sign up page
    - I give my details
    - I can choose between the predefined currency 

#### Log in

- Scenario: I can log into the application
    - I am on the welcome page
    - I give my log in details
    - I click on the Login button
    - I arrive on the Dashboard page
    - I get back toast message when I log in
    
- Scenario: I get back toast message when the username or the password is not correct
    - I am on the welcome page
    - I try to log in with bad credentials
    - I click on the Login button
    - I get back toast message when the username or the password is not correct

- Scenario: I left the fields empty
    - I am on the welcome page
    - I click on the Login button
    - I get feedback about the missing required field
            
#### Log out

- Scenario: I can log out from the application from every page
    - I am on the <test_page>
    - I click on the Sign out button
    - I can sign out
    
|test_page|
:-----:|
|Dashboard|
|View details|
|Search result|

- Scenario: I log out after I close the browser
    - I am on the <test_page>
    - I close my browser
    - I open the application
    - I have to log in again

|test_page|
:-----:|
|Dashboard|
|View details|
|Search result|

#### View Details page

- Scenario: I can navigate into the group
    - I create a group on the Dashboard page
    - I click on the View button
    - I am arrive on the view details page
        
#### Add group item

- Scenario: I can add a group item
    - I am on the dashboard page
    - I click on the Add Group button
    - I chose from the predefined options
    - I click on the add group button on the pop-up
    - The new group is appears on the page
    
- Scenario: I get back feedback about the modification
    - I am on the dashboard page
    - I add a new group
    - A toast message appears about the success 

- Scenario: I can't edit a group if there is an existing group combination (year-month-group combination exist)
    - I am on the dashboard page
    - I add a new group with existing year-month-group combination
    - A toast message appears about the denial 
    
#### Edit group item

- Scenario: I can edit a group item
    - I am on the dashboard page
    - I click on the Edit Group item
    - I change the group details
    - I click on the Edit Group item on the pop-up
    - The modification is successful and I get feedback about the modification

- Scenario: I can't edit a group if it has sub group item
     - I am on the dashboard page
     - I edit a a group and change it for an existing one
     - I get feedback if there is existing sub group under this group
        
- Scenario: I can't edit a group if there is an existing group combination (year-month-group combination exist)
      - I am on the dashboard page
     - I edit a a group and change it for an existing one
     - I get feedback if there is existing group name with the given year-month-group combination 

- Scenario: On the edit pop up there are pre filled field
    - I am on the dashboard page
    - I click on the Edit Group item button
    - On the opening pop-up there are preload data
    
#### Delete group item

- Scenario: I can delete a group item
    - I am on the dashboard page
    - I click on the Delete group item
    - I can delete the actual group item

- Scenario: I get feedback about the modification
    - I am on the dashboard page 
    - I click on the Delete group item
    - I get feedback about the modification

- Scenario: I can't delete a group if it has sub group item
    - I am on the dashboard page 
    - I click on the Delete group item which has sub items
    - I can't delete the group and I get feedback with toast message about the denial 
    
#### Add sub group item

- Scenario: I can give a new group item
    - I am on the view details page
    - I click on the new sub new item
    - I give the details
    - I click on the add button
    - I can save the new sub item

- Scenario: I get toast message feedback after the modification
    - I am on the view details page
    - I add a new sub group item
    - I get back toast message about the success

- Scenario: I left the fields empty
    - I am on the new sub item pop up
    - I click on the add button
    - I get feedback about the missing required field

#### Edit sub group item

- Scenario: I can modify a sub group item
    - I navigate on the view details page
    - I click on the Modify sub item
    - I can modify the chosen Modify sub item

- Scenario: I get toast message feedback after the modification
    - I am on the view details page
    - I edit a sub group item
    - I get back toast message about the success

- Scenario: On the edit pop up there are pre filled field
    - I am on the view details page
    - I click on the modify button
    - There are pre filled field on the pop up (except input value)

#### Delete sub group item

- Scenario: I can delete a sub group item
    - I navigate on the view details page
    - I click on the Remove item
    - I can delete the chosen item

- Scenario: I get toast message feedback after the modification
    - I am on the view details page
    - I delete a sub group item
    - I get back toast message about the success

#### Search

- Scenario: Search field is required
    - I navigate into the dashboard 
    - I left the search field empty
    - I click on the Search button
    - I get feedback about the empty field
    
- Scenario: I can find result based on the given search criteria
    - I navigate into the dashboard 
    - I fill the search field
    - I get back result with table on the search result page 

#### Summarize

- Scenario: I can see the saving on the Dashboard
    - I navigate on the dashboard 
    - I can see the counted available balance on the dashboard


- Scenario: I can see the available balance on the Dashboard
    - I navigate on the dashboard 
    - I can see the counted available balance on the dashboard

- Scenario: I can see sum value on the groups
    - I navigate into the view details
    - I can see the the actual sub group item' sub value
    
#### Charts

- Scenario: I can't see charts until I don't give a group
    - I log into the application
    - I don't have given group and items
    - I can't see the chart

- Scenario: I can see the charts if I have items
    - I log into the application
    - I create a new group and fill up with items
    - I can see the chart 

#### Automated tests

##### GUI Test Automation

For these test I use the google chrome browser. The coverage is cover the main functionality.
Currently these test can run only locally as we need to have Chrome driver to run it.

- Steps to set up:
    - Create test file
    - Download ChromeDriver (latest version: 77.0.3865.40)
    - install selenium with the "pip install selenium" command in the command line
    - run test with "pyton test.py" command in the command line from under the selenium_test folder

- Architect:
    - setUpClass:
        - Initialize runners and open the browsers and redirect to the landing page 
    - tearDownClass:
        - Close the browser

- Test result:
    ![Log in page](selenium_test/test_result.jpg)

## Testing by other people

After I arrived to the testing phase I give the project link to my acquaintance so I could get back honest feedback about the project and bugs

## Testing with different devices

- For the testing my acquaintance and myself we used the follows for testing:
    - Laptops
    - PC
    - Mobile devices
        - Google Pixel 3 (higher resolution)
        - iPhone SE (smaller resolution)
    - Google Chrome browser built in inspector tool
        - Different resolution:
            - HD resolution
            - iPad resolution
            - Different mobile device resolutions

## Testing by different sites

- CSS Validator [link](https://jigsaw.w3.org/css-validator/)
- Responsive design checker [link](http://ami.responsivedesign.is/)
- PEP8 Checker [link](http://pep8online.com)
- Java Script hints [link](https://jshint.com/)