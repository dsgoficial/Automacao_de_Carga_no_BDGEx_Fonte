from time import sleep
from selenium import webdriver

driver = webdriver.Firefox()                        
driver.get('http://bdgexfonte.eb.mil.br/fonte1cgeo')
emailForm = driver.find_element_by_id('username')   
senhaForm = driver.find_element_by_id('password')   
emailForm.send_keys('') #email de cadastro no BDGEx
senhaForm.send_keys('') #senha de cadastro no BDGEx     
botaoEnviar = driver.find_element_by_name('button')
botaoEnviar.click()
produtoMatricial = driver.find_element_by_link_text('Produto Matricial')                                               
produtoMatricial.click()
status = driver.find_element_by_xpath('//select[@name="ativo"]')#formularioPesquisa select.campo')
status.send_keys('Aguardando para importação no banco geo')
pesquisar = driver.find_element_by_id('btnPesquisar')
pesquisar.click()
importarGeo = driver.find_elements_by_class_name('importarmapageo')
while len(importarGeo) > 0:
    importarGeo[0].click()
    sleep(5)
    try:
        close = driver.find_element_by_id('cboxClose')
        close.click()
        sleep(2)
        importarGeo = driver.find_elements_by_class_name('importarmapageo')
    except:
        continue    
    