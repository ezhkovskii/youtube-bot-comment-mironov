from time import sleep
import time, datetime
from random import randint
import threading

from selenium import webdriver

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains


YOUTUBE_LOGIN = 'https://accounts.google.com/signin/v2/identifier?service=youtube'
YOUTUBE_VIDEO = 'https://www.youtube.com/watch?v=mleWEDCNh8s'
EMAIL = ''
PASSWORD = ''
COMMENT = 'Будь счастлив в этот миг. Этот миг и есть твоя жизнь.'

def delay(n):
    sleep(randint(2, n))

def skipAdFunction(skipAd):
    threading.Timer(3,skipAdFunction).start()
    if(skipAd.is_enabled() or skipAd.is_displayed()):
        skipAd.click()

def main():

    driver = webdriver.Chrome('chromedriver.exe')
    driver.set_window_size(1920, 1080)
    driver.get(YOUTUBE_LOGIN)
    delay(5)
    driver.find_element_by_id("identifierId").send_keys(EMAIL)
    driver.find_element_by_id("identifierNext").click()
    delay(2)
    driver.find_element_by_css_selector("input[type=password]").send_keys(PASSWORD)
    driver.find_element_by_id("passwordNext").click()
    delay(5)

    driver.get(YOUTUBE_VIDEO)

    sleep(1)
    duration_text = driver.find_elements_by_xpath("//span[@class='ytp-time-duration']")[0].text
    date_time = datetime.datetime.strptime(duration_text, "%M:%S")
    video_duration_in_seconds = (date_time - datetime.datetime(1900, 1, 1)).total_seconds()

    sleep(5)
    try:
        button = driver.find_element_by_class_name('ytp-ad-skip-button-container')
        button.click()
    except:
        pass

    html = driver.find_element_by_tag_name('html')
    html.send_keys(Keys.PAGE_DOWN)
    sleep(2)

    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-comments ytd-comment-simplebox-renderer")))
    
    driver.find_element_by_css_selector("ytd-comments ytd-comment-simplebox-renderer div#placeholder-area").click()
    my_comment = driver.find_element_by_xpath('//*[@id="contenteditable-root"]')
    my_comment.send_keys('начал смотреть')
    my_comment.send_keys(Keys.CONTROL, Keys.ENTER)

    print('Ждем ', video_duration_in_seconds, ' секунд.')
    #sleep(video_duration_in_seconds)
    sleep(10)

    menu = my_comment.find_element_by_xpath("//div[@class='style-scope ytd-comment-renderer' and @id='action-menu']")
    hover = ActionChains(driver).move_to_element(menu)
    hover.perform()
    menu.click()

    sleep(1)

    WebDriverWait(driver, 5).until(
        EC.presence_of_element_located((By.XPATH, "//yt-formatted-string[@class='style-scope ytd-menu-navigation-item-renderer']")))
    menu.find_element_by_xpath("//yt-formatted-string[@class='style-scope ytd-menu-navigation-item-renderer']").click()
    modified_comment = menu.find_element_by_xpath("/html/body/ytd-app/div/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/ytd-comments/ytd-item-section-renderer/div[3]/ytd-comment-thread-renderer[1]/ytd-comment-renderer/div[4]/ytd-comment-dialog-renderer/ytd-commentbox/div/div[2]/tp-yt-paper-input-container/div[2]/div/div[1]/ytd-emoji-input/yt-user-mention-autosuggest-input/yt-formatted-string/div")
    modified_comment.send_keys(Keys.SHIFT, Keys.HOME)
    modified_comment.send_keys(Keys.DELETE)
    modified_comment.send_keys(COMMENT)
    modified_comment.send_keys(Keys.CONTROL, Keys.ENTER)

    print('Готово')
    sleep(10)


    
if __name__ == "__main__":
    main()
