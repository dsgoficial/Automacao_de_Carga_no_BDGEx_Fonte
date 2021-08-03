#Importa produtos automaticamente com Selenium
import csv
from time import sleep
from selenium import webdriver


class CarregadorProdutos:

    def __init__(self, email, senha, cgeo, caminhocsv=None):
        """
        Construtor da classe Carregador de Produtos
        
        email: email de cadastro no BDGEx
        senha: senha do cadastro no BDGEx
        cgeo: número do CGEO em que será carregado o produto
        caminhocsv: caminho do arquivo csv com os dados dos produtos a serem carregados
        """
        url = 'http://bdgexfonte.eb.mil.br/fonte{}cgeo'.format(str(cgeo))
        self.driver = self.setUp(email, senha, url)
        if caminhocsv:
            self.data = self.openCSVFile(caminhocsv)

    def setUp(self, email, senha, url):
        """
        Faz a configuração inicial do driver do selenium.
        
        email: email de cadastro no BDGEx
        senha: senha do cadastro no BDGEx
        url: endereço da fonte em que será carregado
        
        retorna objeto webdriver.Firefox logado na fonte
        """
        driver = webdriver.Firefox()
        driver.get(url)
        try:
            emailForm = driver.find_element_by_id('username')
            senhaForm = driver.find_element_by_id('password')
            emailForm.send_keys(email)
            senhaForm.send_keys(senha)
            botaoEnviar = driver.find_element_by_name('button')
            botaoEnviar.click()
        except Exception as e:
            return str(e)

        print('Usuário logado')

        return driver

    def openCSVFile(self, csvPath):
        """
        Carrega o CSV com id, caminhoxml, caminhoarquivo [caminhoarquivopdf, 
        completo(True)/sumarizado(False) e área de transferência(True)/local(False)]

        csvPath: caminho do arquivo csv que contém os dados dos arquivos (sem cabeçalho)
        
        retorna dicionário de dicionários, um por uuid, com os caminhos dos arquivos
        """
        data = {}
        with open(csvPath) as csvFile:
            datarows = csv.reader(csvFile)
            for row in datarows:
                columns = row[0].split(';')
                data[columns[0]] = {}
                data[columns[0]]['xml'] = columns[1].replace('"','')
                data[columns[0]]['product'] = columns[2].replace('"','')
                if len(columns) > 3:
                    data[columns[0]]['pdf'] = columns[3].replace('"','')
                    if len(columns) > 4:
                        if columns[4].replace('"','') == 'True':
                            data[columns[0]]['complete'] = True
                        else:
                            data[columns[0]]['complete'] = False
                        if len(columns) > 5:
                            if columns[5].replace('"','') == 'True':
                                data[columns[0]]['transferArea'] = True
                            else:
                                data[columns[0]]['transferArea'] = False                            
                        else:
                            data[columns[0]]['transferArea'] = False #default é False
                    else:
                        data[columns[0]]['complete'] = True #default é True
                        data[columns[0]]['transferArea'] = False #default é False
                else:
                    data[columns[0]]['complete'] = True #default é True
                    data[columns[0]]['transferArea'] = False #default é False

        print('Dados carregados do csv.')

        return data

    def importVectorProduct(self, driver, product):
        """
        Importa um produto vetorial a partir de um xml e um zip
        
        driver: objeto webdriver.Firefox já logado
        product: dicionário {'xml': xmlpath, 'product': zippath, 'complete': True/False}
        
        retorna resultado
        """
        try:
            produtoVetorial = driver.find_element_by_link_text('Produto Vetorial')
            produtoVetorial.click()
            importarNovo = driver.find_element_by_partial_link_text('Importar Novo')
            importarNovo.click()
            if not product['complete']:
                tipoForm = driver.find_element_by_id('tipoform')
                tipoForm.send_keys('sumarizado')
            inputXML = driver.find_element_by_id('arquivo')
            inputXML.send_keys(product['xml'])
            importar = driver.find_element_by_css_selector('#formularioCadastro .continuar')
            importar.click()
            continuarmeta = driver.find_element_by_css_selector('#fMetadados .continuar')
            continuarmeta.click()
            continuarident = driver.find_element_by_css_selector('#fIdentificacao .continuar')
            continuarident.click()
            continuarcarac = driver.find_element_by_css_selector('#fCaracteristicas .continuar')
            continuarcarac.click()
            continuarquali = driver.find_element_by_css_selector('#fQualidade .continuar')
            continuarquali.click()
            if product['transferArea']:
                selecionarArquivoFTP = driver.find_element_by_id('selarquivoftp')
                selecionarArquivoFTP.click()
                nomeArquivo = product['product'].split('/')[-1]
                sleep(1)
                arquivoProduto = driver.find_element_by_link_text(nomeArquivo)
                arquivoProduto.click()
            else:
                arquivoProduto = driver.find_element_by_id('arquivo')
                arquivoProduto.send_keys(product['product'])
                arquivoProduto = driver.find_element_by_id('arquivo')
                arquivoProduto.send_keys(product['product'])
            gravar = driver.find_element_by_css_selector('#fUpload a.continuar')
            gravar.click()
            
            return 'Adicionado'         
        
        except Exception as e:
            return 'Erro: ' + str(e)

    def importRasterProduct(self, driver, product):
        """
        Importa um produto raster a partir de um xml, um tif [e um pdf]
        
        driver: objeto webdriver.Firefox já logado
        product: dicionário {'xml': xmlpath, 'product': tifpath, 'pdf': pdfpath,
                            'complete': True/False, 'transferArea': True/False}
        retorna resultado
        """
        try:
            produtoMatricial = driver.find_element_by_link_text('Produto Matricial')
            produtoMatricial.click()
            importarNovo = driver.find_element_by_partial_link_text('Importar Novo')
            importarNovo.click()
            if not product['complete']:
                tipoForm = driver.find_element_by_id('tipoform')
                tipoForm.send_keys('sumarizado')
            inputXML = driver.find_element_by_id('arquivo')
            inputXML.send_keys(product['xml'])
            importar = driver.find_element_by_css_selector('#formularioCadastro .continuar')
            importar.click()
            continuarmeta = driver.find_element_by_css_selector('#fMetadados .continuar')
            continuarmeta.click()
            continuarident = driver.find_element_by_css_selector('#fIdentificacao .continuar')
            continuarident.click()
            continuarcarac = driver.find_element_by_css_selector('#fCaracteristicas .continuar')
            continuarcarac.click()
            continuarquali = driver.find_element_by_css_selector('#fQualidade .continuar')
            continuarquali.click()
            if product['transferArea']:
                selecionarArquivoFTP = driver.find_element_by_id('selarquivoftp')
                selecionarArquivoFTP.click()
                nomeArquivo = product['product'].split('/')[-1]
                sleep(1)
                arquivoProduto = driver.find_element_by_link_text(nomeArquivo)
                arquivoProduto.click()
            else:
                arquivoProduto = driver.find_element_by_id('arquivo')
                arquivoProduto.send_keys(product['product'])
                arquivoProduto = driver.find_element_by_id('arquivo')
                arquivoProduto.send_keys(product['product'])
            if 'pdf' in product.keys():
                pdf = driver.find_element_by_id('arquivopdf')
                pdf.send_keys(product['pdf'])
            gravar = driver.find_element_by_css_selector('#fUpload a.continuar')
            gravar.click()
            
            return 'Adicionado'         
        
        except Exception as e:
            return 'Erro: ' + str(e)

    def loadProductList(self):
        """
        Carrega produtos da lista passada por csv
        
        self: objeto da classe CarregadorProdutos

        retorna report: relatório de carregamento
        """
        print('Iniciando a carga dos dados.')
        if self.data:
            report = {}
            for count, id in enumerate(self.data.keys()):
                print('Produto sendo carregado('+count+'/'+len(self.data.keys())+'): '+id)
                if '.tif' in self.data[id]['product']:
                    report[id] = self.importRasterProduct(self.driver, self.data[id])
                elif '.zip' in self.data[id]['product']:
                    report[id] = self.importVectorProduct(self.driver, self.data[id])
                else:
                    report[id] = 'Arquivo do produto não é nem tif nem zip.'
                print(report[id])
        else:
            report = 'Não foram carregados dados de produtos ainda.'

        print(report)

        return report

loader = CarregadorProdutos(email='', senha='', cgeo=0, caminhocsv='')
loader.loadProductList()