# =======================
import time
import traceback
import oswa
import spyder.selenium_helper
from selenium.webdriver.common.by import By
import logwa
import logwa.progressbar


speed = 10
timesleep = 60 / speed

browser = spyder.selenium_helper.get_chrome_driver(implicitly_wait=30,headless=False)
# =======================
browser.get(r"https://www.cnvd.org.cn/flaw/typelist?typeId=28")
prog=logwa.progressbar.ProgressBar(87742)


def crawl_1href():
    title = browser.find_element(By.TAG_NAME, 'h1').text
    prog.infof("Crawling :{::rx}", title)
    keys = browser.find_elements(By.XPATH, r'/html/body/div[4]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody//' +
                                 r'td[@class="alignRight"]')
    values = browser.find_elements(By.XPATH, r'/html/body/div[4]/div[1]/div[1]/div[1]/div[2]/div[1]/table/tbody//' +
                                   r'td[not(@class="alignRight")]')
    res = {'title': title}
    for k, v in zip(keys, values):
        res[k.text] = v.text

    return res


def next_page(page):
    xpath = r'/html/body/div[4]/div[1]/div/div[1]/div/*[text()="{}"]'.format(page)

    ele = browser.find_element(By.XPATH, xpath)
    browser.execute_script("arguments[0].click();", ele)


res_all = []


def main():
    for page in range(1, 4389):
        hrefs_len = len(browser.find_elements(By.XPATH, r"//td/a"))
        prog.infof("In page {::gx} ,got hrefs len {::ux}", page, hrefs_len)
        for i in range(0, hrefs_len):
            href = browser.find_elements(By.XPATH, r"//td/a")[i]
            href.click()
            time.sleep(timesleep)
            res=crawl_1href()
            prog.debug(res)
            res_all.append(res)

            browser.back()
            prog.update()
            time.sleep(timesleep)
        if page != 4388:
            next_page(page + 1)
            time.sleep(timesleep)
try:
    logwa.line()
    logwa.info("Start!")
    main()
except Exception as e:
    traceback.print_exc()
    logwa.erro("\n".join(*traceback.extract_tb(e.__traceback__)),e)
    time.sleep(50)
    #logwa.errof("HTML: {}",browser.find_element(By.XPATH,'/html').get_attribute("outerHTML"))
logwa.info("All Done!")
oswa.write('res', str(res_all), cover=True, create=True)
