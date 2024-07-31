
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options  
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from itertools import permutations
from time import sleep 
import datetime
import random
from configLogger import *
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from configLogger import *
import os
from PIL import Image, ImageDraw
import requests
import pandas as pd


def get_driver():
    
    '''
        DESCRIPTION:
            THE DRIVER RETURN. THIS FUNCTION IS USED WHEN SCRAPING IS GOING TO BE PERFORMED ON TWITTER THAT DOES NOT REQUIRE LOGIN.  
    '''
    options = Options()
    options.headless = False
    driver = webdriver.Chrome(ChromeDriverManager().install())
    driver.get('https://www.freepik.es/') 
    return driver


def search_image(words):
    
    driver = get_driver()
    
    # processing word search
    word_search = ''.join([word+'%20' for word in words.split()])[:-3]
    
    #search word
    driver.get('https://www.freepik.es/search?format=search&query='+word_search)
    
    # To make a sleep while to load the page
    sleep(3)
    
    try:        
        # Click to emergency window
        driver.find_elements(By.XPATH, "/html/body/div[8]/div/button")[0].click()
    except:
        pass
    
    return driver
    
def extract_link_image(driver, n):
    
    try:        
        # Click to emergency window
        driver.find_elements(By.XPATH, "/html/body/div[8]/div/button")[0].click()
    except:
        pass
    
    df_total = pd.DataFrame()
    
    for i in range(n):
            
        b = driver.find_element(By.XPATH, '/html/body/main/div[3]/div/div[2]/section')
    
        # Get soup from the page..
        soup_str = b.get_attribute('innerHTML')
        soup = BeautifulSoup(soup_str, features="lxml")
        
        # Extract links from images
        spans_link_image = soup.find_all('img', {'class' : 'landscape loaded'})
        link_images = [span.get("src") for span in spans_link_image]
        
        # To create df with the links of the images images.
        df = pd.DataFrame({'link_image':link_images})
        
        # Concat with of total dataframe
        df_total = pd.concat([df_total, df], axis=0, ignore_index=True)
        
        # To make a sleep
        sleep(2)
        
        try:   
            #  Click to emergency window
            driver.find_elements(By.XPATH, "/html/body/div[4]/div/div/button")[0].click()   
            # To make a sleep
            sleep(2)
        except:
            pass
        
       
        
        # Click on next page
        try:
            
            driver.find_elements(By.XPATH, "/html/body/main/div[3]/div/div[2]/div/div/div[1]/div/a[2]")[0].click()
        except:
            
            driver.find_elements(By.XPATH, "/html/body/main/div[3]/div/div[2]/div/div/div[1]/div/a")[0].click()
        
        # We sleep while the next page loads
        sleep(3)
        
    logger.info(f'A total of {len(df_total)} image links have been extracted.')
        
    return df_total

def create_folder(name_folder):
    if name_folder in os.getcwd():

            directory = os.getcwd()
            
    else:
        os.makedirs(os.getcwd()+"/"+name_folder, exist_ok = True)
        directory = os.getcwd() + "/" + name_folder
        
    return directory
        
        
def download_image(df, directory, namefile):
    
    for idx in df.index:
        
        im = Image.open(requests.get(df.loc[idx, 'link_image'], stream=True).raw)
        #namefile = link.split("?")[0].split("/")[a-1].split(".")[0]
        im = im.save(directory + "/" + namefile + str(idx) + ".jpg")
        # logger.info(f"Finalizado índice {idx}, restan {len(df) - idx}")
        df.loc[idx, 'directory'] = directory + "/" + namefile + str(idx) + ".jpg"
        
    return df

# =============================================================================
# Search image    
# =============================================================================
words = 'happy person'
driver = search_image(words)

# =============================================================================
# Extract all link_image
# =============================================================================
df_total = extract_link_image(driver, 100)

# =============================================================================
# Create directory
# =============================================================================
directory = create_folder('surprise')

# =============================================================================
# Download images
# =============================================================================

df_total = download_image(df_total, directory, 'surprise')