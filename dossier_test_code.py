import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait as WDW
from selenium.webdriver.support import expected_conditions as EC


@pytest.fixture(scope="module")
def project():
    my_project = Options()
    my_project.add_experimental_option("detach", True)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=my_project)
    yield driver
    driver.quit()


@pytest.mark.usefixtures("project")
def test_browser(project):
    # get the url to test
    project.get("http://127.0.0.1:8080/stafflogin/")

    # using the necessary locators to perform desired test
    username = project.find_element(By.ID, "floatingMail")
    username.send_keys("Olagas@gmail.com")
    name_supplied = username.get_attribute('value')
    expected_name = "Olagas@gmail.com"
    assert name_supplied == expected_name, f'{name_supplied} does not match {expected_name}'

    password = project.find_element(By.ID, "password")
    password.send_keys("Obaimole12")

    show_password = project.find_element(By.ID, "showPassword")
    show_password.click()
    assert show_password.is_selected(), 'checkbox was not checked'

    login = project.find_element(By.XPATH, "//button[@type='submit']")
    login.click()

    # wait for the next page to load if the login was successful
    WDW(project, 10).until(
        EC.presence_of_element_located((By.XPATH, "//a[@href='/report']"))
    )
    assert 'staffdashboard' in project.current_url, 'could not login'
    assert '/report' in project.page_source, 'could not login'

    report_page = project.find_element(By.XPATH, "//a[@href='/report']")
    report_page.click()
    assert 'report' in project.current_url, 'unable to redirect to the report page'
    assert 'report' in project.page_source, 'unable to redirect to the report page'

    select_option = project.find_elements(By.XPATH, "//select[@name='workers']/option[@value='2']")
    for opt in select_option:
        val = opt.get_attribute('value')
        if val == '2':
            opt.click()
        assert "2" in val, f'Could not get the same value as {val}'

    text_box = project.find_element(By.XPATH, "//textarea[@name='report']")
    text_box.send_keys('This should be a dummy text report')
    supplied_text = text_box.get_attribute('value')
    expected_text = 'This should be a dummy text report'
    assert supplied_text == expected_text, f'{expected_text} could not be written'

    # click the logout button
    button = project.find_element(By.XPATH, "//a[@href='/stafflogout']")
    button.click()

