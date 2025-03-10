import pickle
import random
import time
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver

def random_sleep(min_sec, max_sec):
    time.sleep(random.uniform(min_sec, max_sec))

def spoof_navigator(driver):
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]})")
    driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")

def login_to_instagram_and_save_cookies(driver, username, password, cookies_file):
    driver.get("https://www.instagram.com/")
    random_sleep(3, 6)
    
    spoof_navigator(driver)
    
    username_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'username')))
    password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, 'password')))
    
    username_input.send_keys(username)
    random_sleep(1, 2)
    password_input.send_keys(password)
    random_sleep(1, 2)
    password_input.send_keys(Keys.RETURN)

    random_sleep(1, 2)

    with open(cookies_file, 'wb') as file:
        pickle.dump(driver.get_cookies(), file)

def login_to_tiktok_and_save_cookies(driver, username, password, cookies_file):
    driver.get("https://www.tiktok.com/login/phone-or-email/email")
    random_sleep(3, 6)
    
    spoof_navigator(driver)
    
    username_input = driver.find_element(By.NAME, 'username')
    password_input = driver.find_element(By.XPATH, "//input[@type='password']")
    
    username_input.send_keys(username)
    random_sleep(1, 2)
    password_input.send_keys(password)
    random_sleep(1, 2)
    password_input.send_keys(Keys.RETURN)
    
    random_sleep(35, 38)

    driver.get("https://www.tiktok.com/login")

    with open(cookies_file, 'wb') as file:
        pickle.dump(driver.get_cookies(), file)

def login_to_youtube_and_save_cookies(driver, email, password, cookies_file, channel_name):
    driver.get("https://www.youtube.com/")

    random_sleep(1, 2)
    
    spoof_navigator(driver)
    
    sign_in_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//*[@aria-label="Sign in"]')))
    sign_in_button.click()
    
    random_sleep(1, 2)
    
    email_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@type="email"]')))
    email_input.send_keys(email)
    random_sleep(1, 2)
    email_input.send_keys(Keys.RETURN)
    
    random_sleep(2, 4)

    password_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//input[@type="password"]')))
    password_input.send_keys(password)
    random_sleep(1, 2)
    password_input.send_keys(Keys.RETURN)

    random_sleep(1, 2)

    try:
        not_but = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Not right now")]')))
        not_but.click()
    except Exception:
        pass
 
    random_sleep(1, 2)

    image = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//img[contains(@alt, "Avatar image")]')))
    driver.execute_script("arguments[0].click();", image)

    random_sleep(1, 2)
    
    switch = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//yt-formatted-string[contains(text(), "Switch account")]')))
    driver.execute_script("arguments[0].click();", switch)

    random_sleep(1, 2)

    channel = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, f'//yt-formatted-string[contains(text(), "{channel_name}")]')))
    driver.execute_script("arguments[0].click();", channel)

    random_sleep(1, 2)

    image = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//img[contains(@alt, "Avatar image")]')))
    driver.execute_script("arguments[0].click();", image)

    random_sleep(1, 2)

    channel = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//a[contains(text(), "View your channel")]')))
    driver.execute_script("arguments[0].click();", channel)

    random_sleep(1, 2)

    channel = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Manage videos")]')))
    driver.execute_script("arguments[0].click();", channel)

    random_sleep(1, 2)

    # Switch to the newly opened tab
    original_window = driver.current_window_handle
    new_window = [window for window in driver.window_handles if window != original_window][0]
    driver.switch_to.window(new_window)

    wait = WebDriverWait(driver, 10)
    settings = wait.until(EC.element_to_be_clickable((By.XPATH, '//tp-yt-paper-icon-item[@id="settings-item"]')))
    driver.execute_script("arguments[0].click();", settings)
    
    random_sleep(1, 2)

    channel = wait.until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Channel")]')))
    driver.execute_script("arguments[0].click();", channel)

    random_sleep(1, 2)

    channel = wait.until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Advanced settings")]')))
    driver.execute_script("arguments[0].click();", channel)

    random_sleep(1, 2)

    element = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//tp-yt-paper-radio-button[@name="NOT_MADE_FOR_KIDS"]')))
    driver.execute_script("arguments[0].click();", element)

    
    random_sleep(1, 2)

    channel = wait.until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Upload defaults")]')))
    driver.execute_script("arguments[0].click();", channel)

    random_sleep(1, 2)

    channel = wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Visibility")]')))
    driver.execute_script("arguments[0].click();", channel)

    random_sleep(1, 2)

    channel = wait.until(EC.presence_of_element_located((By.XPATH, '//yt-formatted-string[contains(text(), "Public")]')))
    driver.execute_script("arguments[0].click();", channel)

    random_sleep(1, 2)

    try: 
        sign_in_button = WebDriverWait(driver, 2).until(EC.presence_of_element_located((By.XPATH, '//*[@aria-label="Got it"]')))
        sign_in_button.click()
    except Exception:
        pass
    
    random_sleep(1, 2)    

    channel = wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(), "Save")]')))
    driver.execute_script("arguments[0].click();", channel)

    random_sleep(1, 2)

    driver.get("https://www.youtube.com/")

    with open(cookies_file, 'wb') as file:
        pickle.dump(driver.get_cookies(), file)

def login_to_snapchat_and_save_cookies(driver, username, password, cookies_file):
    driver.get('https://my.snapchat.com/')
    spoof_navigator(driver)

    sign_in_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign in')]"))
    )
    sign_in_button.click()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[text()='Use phone number instead']"))
    )

    webdriver.ActionChains(driver).send_keys(username).send_keys(Keys.RETURN).perform()

    time.sleep(3)

    webdriver.ActionChains(driver).send_keys(username).send_keys(Keys.RETURN).perform()

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//h1[text()='Enter Password']"))
    )

    webdriver.ActionChains(driver).send_keys(password).send_keys(Keys.RETURN).perform()

    driver.get("https://www.snapchat.com/p/5e7d315a-f401-4f78-b78e-30dc0c06ef49/2044355401445376")

    time.sleep(1)

    with open(cookies_file, 'wb') as file:
        pickle.dump(driver.get_cookies(), file)

def login_to_x_and_save_cookies(driver, email, password, cookies_file):
    driver.get("https://x.com/i/flow/login")
    random_sleep(6, 10)
    
    spoof_navigator(driver)

    iframe = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[title="Sign in with Google Button"]'))
    )
    driver.switch_to.frame(iframe)
    
    sign_in_button = driver.find_element(By.XPATH, '//*[@id="container"]')
    sign_in_button.click()

    time.sleep(3)

    main_window = driver.current_window_handle

    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
    for window_handle in driver.window_handles:
        if window_handle != main_window:
            driver.switch_to.window(window_handle)
            break

    email_input = driver.find_element(By.XPATH, '//input[@type="email"]')
    email_input.send_keys(email)
    random_sleep(1, 2)
    email_input.send_keys(Keys.RETURN)
    
    random_sleep(3, 6)

    password_input = driver.find_element(By.XPATH, '//input[@type="password"]')
    password_input.send_keys(password)
    random_sleep(1, 2)
    password_input.send_keys(Keys.RETURN)

    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(1))
    driver.switch_to.window(main_window)
    
    random_sleep(5, 8)

    driver.get("https://x.com/x")

    time.sleep(1)

    with open(cookies_file, 'wb') as file:
        pickle.dump(driver.get_cookies(), file)

def login_to_linkedin_and_save_cookies(driver, email, password, cookies_file):
    driver.get("https://www.linkedin.com/login")
    random_sleep(6, 10)
    
    spoof_navigator(driver)

    iframe = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[title="Sign in with Google Button"]'))
    )
    driver.switch_to.frame(iframe)
    
    sign_in_button = driver.find_element(By.XPATH, '//*[@id="container"]')
    sign_in_button.click()

    time.sleep(3)

    main_window = driver.current_window_handle

    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(2))
    for window_handle in driver.window_handles:
        if window_handle != main_window:
            driver.switch_to.window(window_handle)
            break

    email_input = driver.find_element(By.XPATH, '//input[@type="email"]')
    email_input.send_keys(email)
    random_sleep(1, 2)
    email_input.send_keys(Keys.RETURN)
    
    random_sleep(3, 6)

    password_input = driver.find_element(By.XPATH, '//input[@type="password"]')
    password_input.send_keys(password)
    random_sleep(1, 2)
    password_input.send_keys(Keys.RETURN)

    WebDriverWait(driver, 10).until(EC.number_of_windows_to_be(1))
    driver.switch_to.window(main_window)
    
    random_sleep(5, 8)

    driver.get("https://www.linkedin.com/feed/")

    time.sleep(1)

    with open(cookies_file, 'wb') as file:
        pickle.dump(driver.get_cookies(), file)

def main():
    pass

if __name__ == "__main__":
    pass