# v.1 2020-11-15
# v.2 2021-05-13
# v.2.1 2021-05-17

# License
# 수정배포를 금지합니다. buy.py을 가지고 수익을 발생하면 민형사상 법적 처벌을 받을 수 있습니다.
# 수정 배포 시 원작자의 주소를 남겨주세요
# 제작자 : https://little-pig.tistory.com/
# 원문 : https://little-pig.tistory.com/entry/11%EB%B2%88%EA%B0%80-%EB%A7%A4%ED%81%AC%EB%A1%9C%EC%98%A4%ED%86%A0%EB%A7%A4%ED%81%AC%EB%A1%9Cselenium%EC%9E%90%EB%8F%99%EA%B5%AC%EB%A7%A4%EC%98%88%EC%95%BD%EA%B5%AC%EB%A7%A4

# 패키지 Import해주세요. 없으면 Error뜹니다_install check
# Import unittest module for creating unit tests
import unittest

# Import time module to implement
import time

# Import the Selenium 2 module (aka "webdriver")
from selenium import webdriver

# For automating data input
from selenium.webdriver.common.keys import Keys

# For providing custom configurations for Chrome to run
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

# Opencv Package
# 다음 패키지도 설치해주세요.
# pip install opencv-python

import pyautogui as pag
from PIL import ImageGrab

# 로그인url
url1 = "https://login.11st.co.kr/auth/login.tmall?returnURL=http%253A%252F%252Fm.11st.co.kr%252FMW%252FMyPage%252FmypageHome.tmall"
# 상품url
url2 = 'http: // www.11st.co.kr / products / 3167879989'

print('페이지 로딩중...')

# Mobile View settings
mobile_emulation = {"deviceName": "iPhone X"}
chrome_options = webdriver.ChromeOptions()


# image Block
# 이미지 블락 처리하면 로딩향상되나 보안패드 숫자도 사라집니다.
# 다른 변수 이용해서 사용가능하신분은 사용하시면 좋아요.
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)

# Mobile View add option
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
# 크롬드라이버 다운로드 주소입니다.
driver = webdriver.Chrome(
    "/Users/mac/Downloads/chromedriver", chrome_options=chrome_options)
# 로그인 페이지 로딩
driver.get(url1)

# PC버전
# send_keys부분에 아이디를 적어주세요
# driver.find_element_by_name('loginName').send_keys('1234')
# send_keys부분에 비밀번를 적어주세요
# driver.find_element_by_name('passWord').send_keys('1234')


# 모바일버전
driver.find_element_by_name('memId').send_keys('1234')
# send_keys부분에 비밀번를 적어주세요
driver.find_element_by_name('memPwd').send_keys('1234')

# time.sleep은 너무빠른 로딩으로 객체를 차지 못할때 발생하는 오류를 줄이기 위함입니다.
# 인터넷 환경이 좀 늦어지는경우에 time.sleep(0)숫자를 올려보세요.
login = driver.find_element_by_class_name("bbtn")
login.click()
print('로그인 완료')
time.sleep(1)
driver.get(url2)
print('구매실행프로세스 대기중')
time.sleep(1)
print('구매실행프로세스 작동시작')

# NVDIA 상품페이지에만 해당하는 클래스 입니다.
# NVDIA RTX 3080 Page Code

while True:
    check = driver.find_element_by_class_name("no_sale")
    if check.text == '현재 판매중인 상품이 아닙니다.':
        driver.refresh()
        print("상품없음 새로고침진행...")
        driver.implicitly_wait(10)

    else:
        buy = driver.find_element_by_name("buy")
        buy.click()
        break
time.sleep(2)

# 이미지 처리를 통한 객체 찾는 방법도 있습니다.
# pyautogui 패키지 입니다. 생각보다 적용하기는 쉬우나 잘 작동하진 않습니다.
else:
        path = r"/User/Desktop/1.png"
        path = pag.locateOnScreen(path)
        if(path is not None):
            getPos = pag.center(path)
            pag.moveTo(getPos)
            pag.click()
            break
time.sleep(2)

# 결제 시스템 부분
# 새로짜야 합니다.
# 무통장 결제가 사라지면서 객체를 받아오질 못하고 있습니다.
#이부분은 pyautogui 패키지를 이용해서 마우스제어로 가능합니다.
# skpay 비밀번호도 pyautogui이걸로 가능하고 확인까지 했습니다.

print("일반결제...")
radio = WebDriverWait(driver, 10).until(EC.visibility_of_element_located(
    (By.XPATH, "//input[@id='payOthers']/following::span[1]")))
driver.execute_script("arguments[0].click();", radio)
noaccount_table = driver.find_element_by_id("paymentGeneralTab5")
print("무통장입금 선택")
noaccount_table.click()
bankKindCtl = driver.find_element_by_id("bankKindCtl04")
bankKindCtl.click()
buying = driver.find_element_by_class_name("btn_order")
buying.click()
print("주문이 완료되었습니다.")
