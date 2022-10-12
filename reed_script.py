from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Details for the bot.
my_email = ''
my_password = ''
cv = ''

# Path for executable stored in driver object
PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)


# Goes to desired website. For this one, the job and location have already been selected before this screen. Saves time
driver.get("https://www.reed.co.uk/jobs/admin-jobs-in-london")

# To maxmimize the window and make finding elements easier
driver.maximize_window()

try:
    cookie = driver.find_element(By.ID, 'onetrust-accept-btn-handler')
    cookie.click()
except:
    pass

signin = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[starts-with(@href,"/account/SignIn")]')))
signin.click()

emailaddress = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'signin_email')))
emailaddress.send_keys(my_email)

password = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'signin_password')))
password.send_keys(my_password)
password.send_keys(Keys.RETURN)

try:
    captcha = WebDriverWait(driver, 2).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="recaptcha-anchor"]/div[1]'))
    )
    captcha.click()
except:
    pass

def applyBot():
    jobs = driver.find_elements(By.XPATH, '//a[@class="gtmJobTitleClickResponsive"]')
    counter = 0
    while (counter < len(jobs)):
        # Get the refreshed elements after each loop to avoid stale exception
        jobs = WebDriverWait(driver, 10).until(
            EC.visibility_of_all_elements_located((By.XPATH, '//a[@class="gtmJobTitleClickResponsive"]'))
            )
        # Scroll to element at current index and click using JavaScript executor, since it's hidden by an element
        driver.execute_script("arguments[0].scrollIntoView();", jobs[counter])
        time.sleep(0.7)
        driver.execute_script("arguments[0].click();", jobs[counter])
        time.sleep(1.5)
        # Checks to see if there's an apply button and clicks. If not, go back and repeat for next job
        applybutton = driver.find_elements(By.XPATH, '//*[@id="applyButtonSide"]')
        if len(applybutton) == 0:
            driver.back()
        else:
            applybutton[0].click()
        # Application sent message
        print(f'{counter} job down')
        counter += 1
        # Repeat
        time.sleep(2)
        driver.back()
        driver.back()



page_count = 1

# Keeps the process going until it can't find any more pages
while True:
    applyBot()
    print(f'Page {page_count} is complete')
    page_count += 1
    try:
        next_page = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="nextPage"]/span/span'))
        )
        next_page.click()
        time.sleep(1.5)
    except:
        print('END OF FINAL PAGE')
        break