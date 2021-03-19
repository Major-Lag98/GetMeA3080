import time

from money_parser import price_dec
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from Alerts import text_alert

PATH = "C:\Program Files (x86)\SeleniumDrivers\chromedriver.exe"    # Make this the path to the driver exe of your choice

driver = webdriver.Chrome(PATH)

email = "email@email.com"
password = "password"
priceLimit = 800

refresh_if_too_expensive = True     # If false program will instead just exit

itemURL = "https://www.amazon.com/dp/B08HR5SXPS?smid=ATVPDKIKX0DER&tag=data20-20#aod"   # Item page you wish to watch

#
# first sign in with email and password
#
driver.get("https://www.amazon.com/ap/signin?openid.pape.max_auth_age=0&openid.return_to=https%3A%2F%2Fwww.amazon.com%2F%3Fref_%3Dnav_ya_signin&openid.identity=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.assoc_handle=usflex&openid.mode=checkid_setup&openid.claimed_id=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0%2Fidentifier_select&openid.ns=http%3A%2F%2Fspecs.openid.net%2Fauth%2F2.0&")

EmailFieldFound = False
completedSignIn = False

print("Signing in")

while not EmailFieldFound or not completedSignIn:

    inputField = driver.find_elements_by_id("ap_email")

    if len(inputField) > 0:
        print("email found")
        EmailFieldFound = True
        field = inputField[0]
        field.send_keys(email)
        field.send_keys(Keys.RETURN)

        PasswordFieldFound = False

        while not PasswordFieldFound:
            inputField = driver.find_elements_by_id("ap_password")

            if len(inputField) > 0:
                print("Password found")
                PasswordFieldFound = True
                field = inputField[0]
                field.send_keys(password)
                field.send_keys(Keys.RETURN)
                completedSignIn = True
                time.sleep(1)
            else:
                print("Password not found")
                driver.refresh()
                break
    else:
        print("Email not found")
        time.sleep(1)
        driver.refresh()

print("Sign in complete")


driver.get(itemURL)     # After signing in go to items page for watching

#
# second check price
#
appropriatePriceFound = False
price = 0
priceIDNames = ["priceblock_ourprice", "price_inside_buybox"]
searchIndex = 0
print("Checking price")
while not appropriatePriceFound:

    priceText = driver.find_elements_by_id(priceIDNames[searchIndex])
    if len(priceText) > 0:
        appropriatePriceFound = True
        price = price_dec(priceText[0].text)    # parse the price string and convert to decimal
        if price < priceLimit:
            print(f"Price is ${price}, which is appropriate")
        else:
            print(f"${price} is too expensive for the limit of ${priceLimit}")
            if refresh_if_too_expensive:
                driver.refresh()
                print("Refreshing")
                appropriatePriceFound = False
            else:
                exit(-1)
    elif searchIndex < len(priceIDNames) - 1:
        #print(f"{priceIDNames[searchIndex]} not found. Trying next")   # Debug
        searchIndex += 1
    else:
        #print(f"{priceIDNames[searchIndex]} not found.")    # Debug
        print("Didn't find price, Item unavailable")
        print("Refreshing")
        driver.refresh()
        time.sleep(1)
        searchIndex = 0

#
# Third, try to buy
#
buttonFound = False
orderConfirmed = False

print("Attempting to buy for: $" + str(price))
while not buttonFound or not orderConfirmed:

    addToCartButton = driver.find_elements_by_id("buy-now-button")

    if len(addToCartButton) > 0:
        buttonFound = True
        print("Buying")
        addToCartButton[0].click()

        #
        #Fourth, confirm your order
        #

        while not orderConfirmed:

            #wait for the confirm iframe to pop up #with a timeout of 5seconds
            WebDriverWait(driver, 5).until(expected_conditions.presence_of_element_located((By.ID, "turbo-checkout-iframe")))
            driver.switch_to.frame(driver.find_element_by_id("turbo-checkout-iframe"))
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
        time.sleep(1)
        driver.refresh()

print("All done")

text_alert(f"Bought a card for ${price}, bot now halting.", "Ten_Digit_Number@txt.att.net")