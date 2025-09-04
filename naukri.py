#Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import time
import random
import datetime
import os



#---Naukri Credentials---
UN = os.getenv("NAUKRI_USER") #Username
PW = os.getenv("NAUKRI_PASS") #Password

# --- Day-wise Profile Summaries (Mon → Sun) ---
SUMMARIES = {
    0: """Data-driven Computer Science graduate specializing in AI and Machine Learning. 
    Experienced in Python, SQL, and data visualization. Proven track record in predictive modeling 
    and analyzing datasets. Seeking roles as Data Scientist/Data Analyst.""",

    1: """Passionate Computer Science graduate with expertise in Machine Learning and Data Analytics. 
    Skilled in Python, SQL, and building data pipelines. Strong problem-solving mindset 
    with hands-on experience in model development and deployment.""",

    2: """Results-oriented graduate with a focus on Artificial Intelligence and Machine Learning. 
    Adept in statistical analysis, predictive modeling, and visualization. Experienced with Python, SQL, 
    and real-world projects. Looking to contribute as a Data Analyst / Data Scientist.""",

    3: """ It' working - Enthusiastic Computer Science professional with strong analytical and technical skills. 
    Specializing in AI, ML, and data-driven solutions. Hands-on experience in Python, SQL, and visualization tools. 
    Eager to apply knowledge in data science and machine learning roles.""",

    4: """Computer Science graduate passionate about applying AI and ML in solving real-world problems. 
    Proficient in Python, SQL, and data analysis. Experienced in developing models and visualizations 
    to derive business insights.""",

    5: """Motivated AI/ML enthusiast with a solid foundation in programming and data science. 
    Skilled in predictive analytics, SQL queries, and visualization dashboards. Seeking opportunities 
    to contribute in impactful projects.""",

    6: """Curious learner and Computer Science graduate, focused on AI, ML, and analytics. 
    Hands-on with Python, SQL, and data modeling. Dedicated to driving data-backed decisions 
    and advancing as a Data Scientist or Analyst."""
}

def log(msg: str):
    """Prints a clean, prefixed log for Github Actions output"""
    print(f"[NAUKRI-BOT] {msg}")

def update_naukri_profile():
    #Setup Chrome
    today = datetime.datetime.today().weekday()
    new_summary = SUMMARIES[today]

    log("Starting Chrome setup...")
    options = webdriver.ChromeOptions()
    options.binary_location = "/usr/bin/google-chrome-stable" #explicit path for GitHub Actions
    options.add_argument("--headless=new")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    
    #driver = webdriver.Chrome(options = options)
    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = options)

    log("Chrome launched succefffully ✅")
    #options.add_argument('--start-maximized')
    
    try:
        #Step 1: Open Naukri
        log("Opening Naukri login page...")
        driver.get('https://www.naukri.com/nlogin/login')

        wait = WebDriverWait(driver, 15)
        
        #Step 2: Enter login details
        log("Filling login form...")
        if not UN or not PW:
            raise ValueError("❌ Naukri credentials not set in environment variables")
        '''driver.find_element(By.ID, 'usernameField').send_keys(UN)
        driver.find_element(By.ID, 'passwordField').send_keys(PW)
        driver.find_element(By.XPATH, "//button[text()='Login']").click()'''

        current_url = driver.current_url

        if "nlogin/login" in current_url:
            username = wait.until(EC.presence_of_element_located((By.ID, "usernameField")))
            password = wait.until(EC.presence_of_element_located((By.ID, "passwordField")))
        elif "nLogin/Login.php" in current_url:
            username = wait.until(EC.presence_of_element_located((By.ID, "emailTxt")))
            password = wait.until(EC.presence_of_element_located((By.ID, "pwd1")))
        else:
            raise RuntimeError(f"Unexpected login page encountered: {current_url}")

        username.send_keys(UN)
        password.send_keys(PW)

        # Wait for login button
        login_button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[text()='Login']")))
        login_button.click()
        
        time.sleep(5)

        #Step 3: Go to profile page
        log("Navigating to profile page...")
        driver.get('https://www.naukri.com/mnjuser/profile')
        time.sleep(5)

        #step 4: Edit Profile Summary
        log("Clicking edit button...")
        edit_button = driver.find_element(By.XPATH, "//h1[contains(text(), 'Profile Summary')]/span[@class='new-pencil']")
        edit_button.click()
        time.sleep(3)

        #Step 5: clear old summary and add new one
        log("Updating summary text...")
        ta = driver.find_element(By.TAG_NAME, 'textarea')
        ta.clear()
        #ta.send_keys(Keys.CONTROL + "a")
        #ta.send_keys(Keys.DELETE)
        ta.send_keys(new_summary)

        #Step 6: Save Changes
        log("Saving changes...")
        save_button = driver.find_element(By.XPATH, "//button[text()='Save']")
        save_button.click()
        time.sleep(3)

        log("Profile summary updated successfully ✅")
        log(f"Today's Summary: {new_summary}")

    except Exception as e:
        log(f"❌ ERROR: {e}")
        # Save screenshot
        try:
            if 'driver' in locals():
                driver.save_screenshot("error_screenshot.png")
                log("Screenshot saved as error_screenshot.png")
        except Exception as ss_e:
            log(f"⚠️ Failed to take screenshot: {ss_e}")

        # Save full traceback to error.log
        with open("error.log", "w") as f:
            f.write(traceback.format_exc())
        log("Error details written to error.log")

        raise  # re-throw to make workflow fail
        
    finally:
        if 'driver' in locals():
            driver.quit()



if __name__ == "__main__":
    update_naukri_profile()


    
        








