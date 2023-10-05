# portfolio

Number Plate Checker
This is my first project. This Python script checks the insurance status of vehicles by inputting their license plates into the "ownvehicle.askmid.com" website and parsing the results. It uses Selenium for web automation and the pypasser library for solving reCAPTCHA challenges.

Usage
Clone this repository to your local machine.

Install the required Python packages if you haven't already. You can use pip for that:


pip install selenium fake_useragent pypasser
Run the script:


python number_plate_checker.py
You will be prompted to enter the number of license plates you want to check and then input each plate one by one.

Description
This script performs the following steps for each license plate:

Launches a headless Chrome browser using Selenium with a randomly generated User-Agent to mimic a real user.
Navigates to the "ownvehicle.askmid.com" website.
Accepts the cookie notice.
Enters the license plate into the search field.
Accepts data protection terms.
Solves any reCAPTCHA challenges using the pypasser library.
Initiates the search.
Parses the results to determine whether the vehicle is insured or not.
If the vehicle is insured, it prints the result and any additional information.
Notes
This script is for educational purposes and should be used responsibly and in compliance with the terms of service of the website.
Make sure you have the Chrome web browser installed and the ChromeDriver executable in your system's PATH or specify its location in the script.
The script uses a headless browser by default. If you want to see the browser window while the script runs, you can remove the --headless option.
Remember that web scraping may be subject to legal restrictions, so always ensure you have the necessary permissions and adhere to the website's terms of service. Good luck with your project!
