from time import sleep
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

driver = webdriver.Firefox()                        
driver.get('http://bdgexfonte.eb.mil.br/fonte1cgeo')
emailForm = driver.find_element_by_id('username')   
senhaForm = driver.find_element_by_id('password')   
emailForm.send_keys('') #email de cadastro no BDGEx
senhaForm.send_keys('') #senha de cadastro no BDGEx           
botaoEnviar = driver.find_element_by_name('button')
botaoEnviar.click()
publicarRecursos = driver.find_element_by_link_text('Publicar Recursos')                                               
publicarRecursos.click()

autorizar = driver.find_elements_by_class_name('autorizar')
while len(autorizar) > 0:
    autorizar[0].click()
    try:
        WebDriverWait(driver, 2).until(EC.alert_is_present())
        sleep(2)
        alert = driver.switch_to.alert
        alert.accept()
        driver.switch_to.default_content()
        sleep(2)
        autorizar = driver.find_elements_by_class_name('autorizar')
    except Exception as e:
        print(e)
        continue 