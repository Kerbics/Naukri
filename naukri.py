#Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import random
import datetime
import os

#---Naukri Credentials---
UN =  os.getenv("USERNAME") #Username
PW = os.getenv("PASSWORD") #Password

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

    3: """Enthusiastic Computer Science professional with strong analytical and technical skills. 
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

def update_naukri_profile():
    #Setup Chrome
    today = datetime.datetime.today().weekday()
    new_summary = SUMMARIES[today]
    
    options = webdriver.ChromeOptions()
    options.add_argument('--start-maximized')
    driver = webdriver.Chrome(service = Service(ChromeDriverManager().install()), options = options)

    try:
        #Step 1: Open Naukri
        driver.get('https://www.naukri.com/nlogin/login')

        #Step 2: Enter login details
        driver.find_element(By.ID, 'usernameField').send_keys(UN)
        driver.find_element(By.ID, 'passwordField').send_keys(PW)
        driver.find_element(By.XPATH, "//button[text()='Login']").click()
        time.sleep(5)

        #Step 3: Go to profile page
        driver.get('https://www.naukri.com/mnjuser/profile')
        time.sleep(5)

        #step 4: Update Profile
        edit_button = driver.find_element(By.XPATH, "//h1[contains(text(), 'Profile Summary')]/span[@class='new-pencil']")
        edit_button.click()
        time.sleep(3)

        #Step 5: clear old summary and add new one
        ta = driver.find_element(By.TAG_NAME, 'textarea')
        ta.send_keys(Keys.CONTROL + "a")
        ta.send_keys(Keys.DELETE)
        ta.send_keys(new_summary)

        #Step 6: Save Changes
        save_button = driver.find_element(By.XPATH, "//button[text()='Save']")
        save_button.click()
        time.sleep(3)

        print('✅ Profile summary updated successfully!')

    except Exception as e:
        print('❌ Error:', e)
    finally:
        driver.quit()



if __name__ == "__main__":
    update_naukri_profile()


    
        

