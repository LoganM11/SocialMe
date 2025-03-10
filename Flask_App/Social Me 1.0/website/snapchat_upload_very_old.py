import time
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
import pyautogui


def read_description(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.readline().strip()
    
def spoof_navigator(driver):
    driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
    driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3]})")
    driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")

def upload_video(driver, video_path, description, username, password):
    #class ant-btn sds-button regular sds-base-button primary
    try:
        print("Navigating to Snapchat...")
        driver.get('https://my.snapchat.com/')
        spoof_navigator(driver)

        print("Waiting for 'Sign in' button to be clickable...")
        sign_in_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Sign in')]"))
        )
        sign_in_button.click()
        print("'Sign in' button clicked.")
        time.sleep(3)
        print("Waiting for 'Use phone number instead' option to appear...")
        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//a[text()='Use phone number instead']"))
        )
        print("'Use phone number instead' option found.")

        print("Entering username...")
        webdriver.ActionChains(driver).send_keys(username).send_keys(Keys.RETURN).perform()

        time.sleep(3)  # Delay for input field readiness
        print("Re-entering username to ensure input...")
        webdriver.ActionChains(driver).send_keys(username).send_keys(Keys.RETURN).perform()

        print("Waiting for password entry screen...")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[text()='Enter Password']"))
        )
        print("Password entry screen ready.")

        print("Entering password...")
        webdriver.ActionChains(driver).send_keys(password).send_keys(Keys.RETURN).perform()

        print(video_path)

        # Use PyAutoGUI to interact with the file dialog
        print("Sending file path...")
        file_input = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='file'][accept='video/mp4,video/quicktime,video/webm,image/jpeg,image/png']"))
        )
        file_input.send_keys(video_path)

        post_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "/html/body/div/main/div[2]/div[2]/div[2]/div[5]/div[1]/div[1]/div/div[2]/div/div/div/div[1]/div/div/div/div[1]"))
        )
        post_button.click()

        print("Waiting for 'Post to Spotlight' button...")
        post_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//div[text()='Post to Spotlight']"))
        )
        driver.execute_script("arguments[0].click();", post_button)
        print("'Post to Spotlight' button clicked.")

        print("Waiting for description textarea...")
        description_textarea = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "//textarea[@placeholder='Add a description and #topics']"))
        )
        print("Description textarea found.")
        description_textarea.send_keys(description)
        print(f"Description added: {description}")
        

        print("Looking for 'Agree to Spotlight Terms' button...")
        agree_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Agree to Spotlight Terms')]"))
        )
        agree_button.click()
        print("'Agree to Spotlight Terms' button clicked.")
        
        try:
            print("Checking for an additional 'Accept' button...")
            accept_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, "//button[@class='ant-btn sds-button regular sds-base-button primary']"))
            )
            accept_button.click()
            print("Second 'Accept' button clicked.")
        except Exception as e:
            print(f"Second 'Accept' button not found. Continuing without clicking it. Error: {e}")

        time.sleep(3)
        print("Waiting for 'Post to Snapchat' button...")
        post_final_button = WebDriverWait(driver, 20).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Post to Snapchat')]"))
        )

        post_final_button.click()

        print("post button clicked")

        print("waiting to finish uploading")
        WebDriverWait(driver, 120).until(
            EC.presence_of_element_located((By.XPATH, "//div[text()='Yay! Your post is now live!']"))
        )
        print("Upload success message detected. Closing the browser.")

        time.sleep(2)

    except Exception as e:
        print(f"An error occurred: {e}")
        raise  

    finally:
        driver.quit()

def main(video_path, cookies_file, channel_name, title, description, tags, username, password):    
    options = uc.ChromeOptions()
    options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36")
    options.add_argument("--disable-blink-features=AutomationControlled")
    driver = uc.Chrome(options=options)
    

    try:
        upload_video(driver, video_path, description, username, password)
    finally:
        driver.quit()

if __name__ == "__main__":
    pass