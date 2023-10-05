import time

from selenium import webdriver

from pypasser import reCaptchaV2
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent


number_plates=[]

qty = int(input("How many number plates? "))
for b in range(qty):
    plate=input("Enter plate: ")
    number_plates.append(plate)








for plates in number_plates:
    options = Options()
    ua = UserAgent()
    user_agent = ua.random
    options.add_argument(f'--user-agent={user_agent}')
    options.add_argument('--headless')
    driver = webdriver.Chrome(options=options)
    driver.get("https://ownvehicle.askmid.com/")
    time.sleep(1)
    driver.find_element(By.ID,"acceptCookieBtn").click()
    driver.find_element(By.CLASS_NAME,"form-control").send_keys(str(plates))
    driver.find_element(By.ID, "chkDataProtection").click()
    time.sleep(1)
    url = driver.find_element(By.XPATH,'//*[@id="leftDiv"]/div/div[3]/div/div/div/iframe').get_attribute("src")
    time.sleep(2)
    driver.find_element(By.ID,"btnCheckVehicle").click()
    time.sleep(2)
    is_checked = reCaptchaV2(driver)
    time.sleep(1)
    driver.find_element(By.ID, "btnCheckVehicle").click()
    time.sleep(3)
    final = driver.find_element(By.CLASS_NAME,"well").find_element(By.TAG_NAME,"h4")
    print(f"{plates} {final.text}")
    if final.text == "YES. This vehicle is showing as INSURED on the Motor Insurance Database today":
        car_info=driver.find_element(By.CLASS_NAME,"well").find_elements(By.TAG_NAME,"p")
        for info in car_info:
            print(info.text)
            print(f"Finish {plates} ")


    driver.close()







