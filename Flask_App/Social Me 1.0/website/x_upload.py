import pickle
import random
import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def random_sleep(min_sec, max_sec):
    time.sleep(random.uniform(min_sec, max_sec))

def spoof_navigator(driver):
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]})")
    driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")
    driver.execute_script("Object.defineProperty(navigator, 'platform', {get: () => 'Win32'})")
    driver.execute_script("Object.defineProperty(navigator, 'deviceMemory', {get: () => 8})")
    driver.execute_script("Object.defineProperty(navigator, 'hardwareConcurrency', {get: () => 4})")

def read_description(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read(280)

def load_cookies(driver, cookies_file):
    driver.get("https://x.com/x")
    spoof_navigator(driver)
    with open(cookies_file, 'rb') as file:
        cookies = pickle.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
    driver.refresh()
    random_sleep(3, 5)

def upload_video(driver, video_path, description):
    driver.get("https://x.com/compose/post")
    spoof_navigator(driver)

    try:
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//input[@type="file"]'))
        )
        file_input.send_keys(video_path)
        time.sleep(10)
    except Exception as e:
        print("File input send keys failed:", e)
        return

    try:
        description_box = WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//*[@role="textbox"]'))
        )
        description_box.send_keys(description)
        time.sleep(1)
    except Exception as e:
        print("Description input failed:", e)

    WebDriverWait(driver, 120).until(
        EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Uploaded')]"))
    )

    try:
        post_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@data-testid, 'tweetButton') and .//span[text()='Post']]"))
        )
        post_button.click()
    except Exception as e:
        print("Post sharing failed:", e)
    
    try:
        time.sleep(5)
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'published')]"))
        )
        print("Upload success message detected. Closing the browser.")
    except Exception as e:
        print("Failed to detect published stage message:", e)

def main(video_path, cookies_file, channel_name, title, description, tags, username, password):    
    options = uc.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36")
    driver = uc.Chrome(options=options)

    try:
        load_cookies(driver, cookies_file)
        upload_video(driver, video_path, description, title, tags)
    finally:
        driver.quit()

if __name__ == "__main__":
    pass