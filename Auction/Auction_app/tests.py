




# from django.test import TestCase

# # Create your tests here.
# from datetime import datetime
# from django.test import TestCase
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# class Hosttest(TestCase):
    
#     def setUp(self):
#         self.driver = webdriver.Chrome()
#         self.driver.implicitly_wait(10)
#         self.live_server_url = 'http://127.0.0.1:8000/'

#     def tearDown(self):
#         self.driver.quit()
        
#     def test_01_login_page(self):
#         driver = self.driver
#         driver.get(self.live_server_url)
#         driver.maximize_window()
#         time.sleep(1)
#         login=driver.find_element(By.CSS_SELECTOR,"a.getstarted.scrollto[href='/auth_app/handlelogin']")
#         login.click()
#         time.sleep(2)
#         email=driver.find_element(By.CSS_SELECTOR,"input[type='email'][name='email']")
#         email.send_keys("cheenku123@gmail.com")
#         password=driver.find_element(By.CSS_SELECTOR,"input[type='password'][name='password']")
#         password.send_keys("Suppi@123")
#         time.sleep(2)
#         submit=driver.find_element(By.CSS_SELECTOR,"button#login.btn.btn-signin.btn-block")
#         submit.click()
#         time.sleep(2)

       
#         dropdown_menu = driver.find_element(By.CLASS_NAME, "dropdown")
#         dropdown_menu.click()
#         time.sleep(2)

#         order_details_link = WebDriverWait(driver, 10).until(
#         EC.element_to_be_clickable((By.XPATH, "//li[@class='dropdown']//a[text()='Order Details']")))
#         order_details_link.click()
#         time.sleep(2)

#         add_review_button = WebDriverWait(driver, 10).until( EC.element_to_be_clickable((By.CLASS_NAME, "btn-primary")))
#         driver.execute_script("arguments[0].click();", add_review_button)
#         add_review_modal = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "addReviewModal")))
#         time.sleep(2)

#         review_textarea = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.NAME, "review_text")))
#         review_textarea.clear()

#         review_text = "Content seller was good"
#         review_textarea.send_keys(review_text)
#         time.sleep(2)


#         submit_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, "//input[@type='submit' and @value='Submit Review']")))
#         submit_button.click()
#         time.sleep(2)










# Add  blog




# from django.test import TestCase

# # Create your tests here.
# from datetime import datetime
# from django.test import TestCase
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# class Hosttest(TestCase):
    
#     def setUp(self):
#         self.driver = webdriver.Chrome()
#         self.driver.implicitly_wait(10)
#         self.live_server_url = 'http://127.0.0.1:8000/'

#     def tearDown(self):
#         self.driver.quit()
        
#     def test_01_login_page(self):
#         driver = self.driver
#         driver.get(self.live_server_url)
#         driver.maximize_window()
#         time.sleep(1)
#         login=driver.find_element(By.CSS_SELECTOR,"a.getstarted.scrollto[href='/auth_app/handlelogin']")
#         login.click()
#         time.sleep(2)
#         email=driver.find_element(By.CSS_SELECTOR,"input[type='email'][name='email']")
#         email.send_keys("sreeharij28200@gmail.com")
#         password=driver.find_element(By.CSS_SELECTOR,"input[type='password'][name='password']")
#         password.send_keys("Sreeh@ri123")
#         time.sleep(2)
#         submit=driver.find_element(By.CSS_SELECTOR,"button#login.btn.btn-signin.btn-block")
#         submit.click()
#         time.sleep(2)


#         add_blog_link = driver.find_element(By.CSS_SELECTOR, "a.btn.btn-primary[href='/add/']")
#         add_blog_link.click()
#         time.sleep(2)

#         heading_input = driver.find_element(By.ID, "id_heading")
#         heading_input.clear()  
#         heading_input.send_keys("My Blog Heading") 
#         time.sleep(2)
         

#         description_textarea = driver.find_element(By.ID, "id_description")
#         description_textarea.clear()  
#         description_textarea.send_keys("Blogs are a type of regularly updated websites that provide insight into a certain topic. The word blog is a combined version of the words “web” and “log.” At their inception, blogs were simply an online diary where people could keep a log about their daily lives on the web.")
#         time.sleep(2)
        
#         image_input = driver.find_element(By.ID, "id_image")
#         image_input.send_keys("C:\\Users\\Sreehari\\Downloads\\view.jpg")
#         time.sleep(2)




        

#         btn=driver.find_element(By.CSS_SELECTOR,"button.btn.btn-primary[type='submit']")
#         btn.click()
#         time.sleep(2)









 #CHAT TESTING

# from django.test import TestCase

# # Create your tests here.
# from datetime import datetime
# from django.test import TestCase
# from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# import time
# from selenium.webdriver.common.by import By
# from selenium.webdriver.common.action_chains import ActionChains
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# class Hosttest(TestCase):
    
#     def setUp(self):
#         self.driver = webdriver.Chrome()
#         self.driver.implicitly_wait(10)
#         self.live_server_url = 'http://127.0.0.1:8000/'

#     def tearDown(self):
#         self.driver.quit()
        
#     def test_01_login_page(self):
#         driver = self.driver
#         driver.get(self.live_server_url)
#         driver.maximize_window()
#         time.sleep(1)
#         login=driver.find_element(By.CSS_SELECTOR,"a.getstarted.scrollto[href='/auth_app/handlelogin']")
#         login.click()
#         time.sleep(2)
#         email=driver.find_element(By.CSS_SELECTOR,"input[type='email'][name='email']")
#         email.send_keys("cheenku123@gmail.com")
#         password=driver.find_element(By.CSS_SELECTOR,"input[type='password'][name='password']")
#         password.send_keys("Suppi@123")
#         time.sleep(2)
#         submit=driver.find_element(By.CSS_SELECTOR,"button#login.btn.btn-signin.btn-block")
#         submit.click()
#         time.sleep(2)


#         live=driver.find_element(By.CSS_SELECTOR,"a.nav-link.scrollto[href='/live-auctions/']")
#         live.click()
#         time.sleep(2)

#         bid=driver.find_element(By.CSS_SELECTOR,"a#bidding.btn.btn-danger[href='/product/22/' ]")
#         bid.click()
#         time.sleep(2)

#         chat=driver.find_element(By.CSS_SELECTOR,"a.button[href='/chat/']")
#         chat.click()
#         time.sleep(2)

#         roomtext=driver.find_element(By.CSS_SELECTOR,"input#input-message.form-control.type_msg")
#         roomtext.send_keys("hi hello")
#         time.sleep(2)

#         btn=driver.find_element(By.CSS_SELECTOR,"button.btn.btn-secondary[type='submit']")
#         btn.click()
#         time.sleep(2)





