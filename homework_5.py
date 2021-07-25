import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from pymongo import MongoClient

MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_DB = 'posts'
MONGO_COLLECTION = 'posts_collection'

DRIVER_PATH = "./chromedriver"
url = "https://vk.com/tokyofashion"

desired_tag = input('Enter the desired tag: ')

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(DRIVER_PATH, options=options)

driver.get(url)
driver.find_element_by_xpath('//body').send_keys(Keys.CONTROL, Keys.END)

button_class = "JoinForm__notNow"
try:
    button = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.CLASS_NAME, button_class)))
    button.send_keys(Keys.ENTER)
except Exception as e:
    print(e)

for scroll in range(3):
    time.sleep(2)
    driver.find_element_by_xpath('//body').send_keys(Keys.CONTROL, Keys.END)

time.sleep(10)
button_class = 'ui_tab_plain ui_tab_search'

activate_search = driver.find_element_by_xpath('//li[contains(@class, "ui_tab_search_wrap")]/a[contains(@class, "ui_tab_plain ui_tab_search")]')
activate_search.send_keys(Keys.ENTER)
getted_posts = driver.find_element_by_id('wall_search')
getted_posts.send_keys(desired_tag)
getted_posts.send_keys(Keys.ENTER)

time.sleep(5)
posts_path = '//div[contains(@class, "_post post page_block post--with-likes closed_comments deep_active")]'
posts = driver.find_elements_by_xpath(posts_path)

time.sleep(5)
posts_info =[]
for post in posts:
    info = {}
    try:
        post_date = post.find_element_by_class_name('rel_date')
        info["date"] = post_date.text
    except Exception as e:
        info["date"] = None

    try:
        post_text = post.find_element_by_class_name('wall_post_text')
        info["text"] = post_text.text.replace('\n\n', ' ')
    except Exception as e:
        info["text"] = None

    try:
        post_link = post.find_element_by_class_name('post_link')
        info["post_link"] = post_link.get_attribute('href')
    except Exception as e:
        info["post_link"] = None

    try:
        image_link = post.find_element_by_class_name('page_post_thumb_wrap')
        info["image_link"] = image_link.get_attribute('href')
    except Exception as e:
        info["image_link"] = None

    try:
        likes_count = post.find_element_by_class_name('_like')
        info["likes_count"] = likes_count.get_attribute('data-count')
    except Exception as e:
        info["likes_count"] = None

    try:
        shares_count = post.find_element_by_class_name('_share')
        info["shares_count"] = shares_count.get_attribute('data-count')
    except Exception as e:
        info["shares_count"] = None

    try:
        views_count = post.find_element_by_class_name('like_views')
        info["views_count"] = views_count.text
    except Exception as e:
        info["views_count"] = None

    posts_info.append(info)

with MongoClient(MONGO_HOST, MONGO_PORT) as client:
    db = client[MONGO_DB]
    posts = db[MONGO_COLLECTION]
    posts.insert_many(posts_info)

driver.quit()