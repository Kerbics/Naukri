#Imports
from playwright.sync_api import sync_playwright
import datetime
import os

# --- Naukri Credentials ---
UN = os.getenv("NAUKRI_USER")
PW = os.getenv("NAUKRI_PASS")

# --- Day-wise Summaries ---
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


def update_naukri_profile():
    today = datetime.datetime.today().weekday()
    new_summary = SUMMARIES[today]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        print("[NAUKRI-BOT] Opening Naukri login page...")
        page.goto("https://www.naukri.com/nlogin/login")

        if not UN or not PW:
            raise ValueError("❌ Naukri credentials not set in environment variables")

        print("[NAUKRI-BOT] Logging in...")
        if page.locator("#usernameField").count() > 0:
            page.fill("#usernameField", UN)
            page.fill("#passwordField", PW)
        elif page.locator("#emailTxt").count() > 0:
            page.fill("#emailTxt", UN)
            page.fill("#pwd1", PW)
        else:
            raise RuntimeError("❌ Could not find login fields")

        page.click("button:has-text('Login')")
        page.wait_for_timeout(5000)

        print("[NAUKRI-BOT] Navigating to profile page...")
        page.goto("https://www.naukri.com/mnjuser/profile")
        page.wait_for_timeout(5000)

        print("[NAUKRI-BOT] Updating summary...")
        page.click("xpath=//h1[contains(text(),'Profile Summary')]/span[@class='new-pencil']")
        textarea = page.locator("textarea")
        textarea.fill(new_summary)
        page.click("button:has-text('Save')")
        page.wait_for_timeout(3000)

        print("[NAUKRI-BOT] ✅ Profile summary updated successfully")
        print(f"[NAUKRI-BOT] Today's Summary: {new_summary}")

        browser.close()

if __name__ == "__main__":
    update_naukri_profile()
