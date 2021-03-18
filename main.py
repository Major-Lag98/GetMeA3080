import time

from money_parser import price_dec
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys

PATH = "C:\Program Files (x86)\SeleniumDrivers\chromedriver.exe"

driver = webdriver.Chrome(PATH)

email = "email@email.com"
password = "password"
priceLimit = 800

# first sign in with email and password
driver.get("https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&")

EmailFieldFound = False
completedSignIn = False

print("Signing in")

while not EmailFieldFound or completedSignIn:

    inputField = driver.find_elements_by_id("ap_email")

    if len(inputField) > 0:
        print("email found")
        EmailFieldFound = True
        field = inputField[0]
        field.send_keys(email)
        field.send_keys(Keys.RETURN)
        # time.sleep(3)

        PasswordFieldFound = False

        while not PasswordFieldFound:
            inputField = driver.find_elements_by_id("ap_password")

            if len(inputField) > 0:
                print("Password found")
                PasswordFieldFound = True
                field = inputField[0]
                field.send_keys(password)
                field.send_keys(Keys.RETURN)
                time.sleep(1)
            else:
                print("Password not found")
                driver.refresh()
                break
    else:
        print("Email not found")
        time.sleep(100)
        driver.refresh()

print("Sign in complete")


# Test a link that's unavailable and one that's available

# Bad link
#driver.get("https://www.amazon.com/dp/B08HH5WF97?smid=ATVPDKIKX0DER&tag=data20-20#aod")

# Good link expensive
#driver.get("https://www.amazon.com/Gaming-GeForce-Graphics-DisplayPort-Bearings/dp/B08YBB228Y/ref=sr_1_1_sspa?crid=3MTLIS53NPC42&dchild=1&keywords=rtx+3080&qid=1616024327&sprefix=rtx%2Caps%2C230&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyUU4yRzZLT1VXWUxPJmVuY3J5cHRlZElkPUEwMTgwNDQ0M0NPSUlXQzlSUTlVUSZlbmNyeXB0ZWRBZElkPUEwOTI4MzIyMkNSN1lES1U4NUlWQyZ3aWRnZXROYW1lPXNwX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU=")

# good link cheap
#driver.get("https://www.amazon.com/Paulas-Choice-SKIN-PERFECTING-Exfoliant-Facial-Blackheads/dp/B07C5SS6YD/ref=sr_1_13?dchild=1&keywords=exfoliation%2Bcream&qid=1616032354&sr=8-13&th=1")

driver.get("https://www.amazon.com/dp/B07C5SS6YD/ref=twister_B01JGVQ3SQ?_encoding=UTF8&psc=1")


# second check price
priceFound = False
price = 0
priceIDNames = ["priceblock_ourprice", "price_inside_buybox"]
searchIndex = 0
print("Checking price")
while not priceFound:

    priceText = driver.find_elements_by_id(priceIDNames[searchIndex])
    if len(priceText) > 0:
        priceFound = True
        price = price_dec(priceText[0].text)
        if price < priceLimit:
            print("Price is nominal")
        else:
            print("Too expensive")
            exit(-1)
    else:
        print(priceIDNames[searchIndex] + " not found. Trying next")
        searchIndex += 1

# Third, try to buy

buttonFound = False
orderConfirmed = False

print("Attempting to buy for: $" + str(price))
while not buttonFound or not orderConfirmed:

    addToCartButton = driver.find_elements_by_id("buy-now-button")

    if len(addToCartButton) > 0:
        buttonFound = True
        print("Buying")
        addToCartButton[0].click()
        WebDriverWait(driver, 10).until(expected_conditions.presence_of_element_located((By.ID, "turbo-checkout-iframe")))
        driver.switch_to.frame(driver.find_element_by_id("turbo-checkout-iframe"))

        #Fourth, confirm order

        while not orderConfirmed:

            #driver.switch_to.frame()
            placeOrderButton = driver.find_elements_by_id("turbo-checkout-pyo-button")

            print("The length is " + str(len(placeOrderButton)))

            if len(placeOrderButton) > 0:
                orderConfirmed = True
                placeOrderButton[0].click()
                print("Clicked confirm")
            else:
                print("Something went wrong")
                driver.refresh()
                break

    else:
        time.sleep(3)
        driver.refresh()

print("All done")


