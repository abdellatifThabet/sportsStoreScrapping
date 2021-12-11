from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from time import time, sleep
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--no-sandbox')
chrome_options.headless = True
chrome_options.add_argument("--disable-notifications")
chrome_options.add_argument("--start-maximized")
#chrome_options.add_argument("--disable-dev-shm-usage")
from selenium.webdriver.common.by import By 
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.keys import Keys
import pandas as pd

driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
wait = WebDriverWait(driver, 10)

url = 'https://www.grupocoas.com/shop'
driver.get(url)

df = pd.DataFrame(columns=['product_name','product_image','brand_name','model','profile','price','reference_code','color','ref_gcs','type','size','component','sizing'])


done = True
st = 0
while(done):
    products = wait.until(EC.presence_of_all_elements_located((By.XPATH, "/html/body/div[2]/main/div[1]/div[3]/div[3]/div[2]/table/tbody/tr/td")))
    for i, product in enumerate(products):
        try:
        ## from home page
            product_image = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/div[1]/div[3]/div[3]/div[2]/table/tbody/tr/td["+str(i+1)+"]/div/form/div/div/a/span/img"))).get_attribute("src")
            brand_name = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/div[1]/div[3]/div[3]/div[2]/table/tbody/tr/td["+str(i+1)+"]/div/form/div/section/h6/a[2]"))).text
            model = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/div[1]/div[3]/div[3]/div[2]/table/tbody/tr/td["+str(i+1)+"]/div/form/div/section/h6/a[3]"))).text
            profile = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/div[1]/div[3]/div[3]/div[2]/table/tbody/tr/td["+str(i+1)+"]/div/form/div/section/h6/a[4]"))).text
        
            ############## going to details page ***************
            next_prod = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/div[1]/div[3]/div[3]/div[2]/table/tbody/tr/td["+str(i+1)+"]/div/form/div/div/a"))).get_attribute("href")
        except:
            continue
        try:
            driver.execute_script("window.open('" +next_prod +"');")
            # switch to new window
            driver.switch_to.window(driver.window_handles[1])
            ## from details page
            product_name = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/div[1]/section[1]/div[2]/div[3]/div/div[1]/h1"))).text
            price = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/div[1]/div[2]/form/div/div[2]/div/h4[1]/b/span"))).text
            #reference_label = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/div[1]/section[1]/div[2]/div[3]/div/div[1]/strong[3]"))).text
            #if(reference_label == 'Ref.:'):
            reference_code = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/div[1]/section[1]/div[2]/div[3]/div/div[1]/span[4]"))).text
            color = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/div[1]/section[1]/div[2]/div[3]/div/div[1]/span[5]"))).text
            ref_gcs = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/div[1]/section[1]/div[2]/div[3]/div/div[1]/span[7]"))).text

            wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/div[1]/div[3]/div/ul/li[2]/a"))).click()
            Type = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/div[1]/section[2]/div/div/table/tbody/tr[1]/td[2]"))).text
            size = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/div[1]/section[2]/div/div/table/tbody/tr[4]/td[2]"))).text
            component = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/div[1]/section[2]/div/div/table/tbody/tr[6]/td[2]"))).text
            sizing = wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/div[1]/section[2]/div/div/table/tbody/tr[8]/td[2]"))).text
            df.loc[st] = [product_name, product_image, brand_name, model, profile, price, reference_code, color, ref_gcs,Type,size,component,sizing]
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
        except:
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            continue
        st = st+1
    print(str(st)+' products extracted ...')
    try:    
        wait.until(EC.presence_of_element_located((By.XPATH, "/html/body/div[2]/main/div[1]/div[3]/div[3]/div[2]/div/ul/li[9]/a"))).click()
    except:
        done = False
        print('all data extracted')

df.to_csv('coasport-data.csv', index=False)