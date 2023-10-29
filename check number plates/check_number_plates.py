import time
from selenium import webdriver
from pypasser import reCaptchaV2
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent

# Initialize an empty list to store vehicle license plates
number_plates = []


# Ask the user for the number of license plates they want to check
qty = int(input("How many number plates? "))
for b in range(qty):
    # Ask the user to input a license plate and add it to the list
    plate = input("Enter plate: ")
    number_plates.append(plate)

# Loop through the list of license plates
for plates in number_plates:
    options = Options()
    ua = UserAgent()
    user_agent = ua.random
    options.add_argument(f'--user-agent={user_agent}')
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    
    # Open the website for checking vehicle insurance status
    driver.get("URL")
    time.sleep(1)
    
    # Accept cookies button
    driver.find_element(By.ID,"acceptCookieBtn").click()
    
    # Enter the license plate number into the form
    driver.find_element(By.CLASS_NAME,"form-control").send_keys(str(plates))
    
    # Check the data protection checkbox
    driver.find_element(By.ID, "chkDataProtection").click()
    time.sleep(1)
    
    # Get the URL of the reCAPTCHA iframe
    url = driver.find_element(By.XPATH,'//*[@id="leftDiv"]/div/div[3]/div/div/div/iframe').get_attribute("src")
    time.sleep(2)
    
    # Click the "Check Vehicle" button
    driver.find_element(By.ID,"btnCheckVehicle").click()
    time.sleep(2)
    
    # Check if a CAPTCHA is encountered and solve it using pypasser's reCaptchaV2 function
    is_checked = reCaptchaV2(driver)
    time.sleep(1)
    
    # Click the "Check Vehicle" button again
    driver.find_element(By.ID, "btnCheckVehicle").click()
    time.sleep(3)
    
    # Get the result message from the website
    final = driver.find_element(By.CLASS_NAME,"well").find_element(By.TAG_NAME,"h4")
    
    # Print the result of the license plate check
    print(f"{plates} {final.text}")
    
    # If the vehicle is insured, print additional information
    if final.text == "YES. This vehicle is showing as INSURED on the Motor Insurance Database today":
        car_info = driver.find_element(By.CLASS_NAME,"well").find_elements(By.TAG_NAME,"p")
        for info in car_info:
            print(info.text)
    
    # Close the Chrome WebDriver
    driver.close()
