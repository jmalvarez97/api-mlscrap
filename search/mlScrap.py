from flask import Flask, request, jsonify
import json
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from lxml import html
import requests




def quitarAcentos(str):
  return str.lower().replace('á', 'a').replace('é','e').replace('í', 'i').replace('ó', 'o').replace('ú', 'u')

def obtenerFeatures(source):
  '''
  Recibe el source de la pagina y busca las caracteristicas del articulo
  '''
  cat = quitarAcentos(source.xpath('//a[@class="ui-pdp-syi__link"]')[0].text_content())
  if "vehiculo" in cat:
    path_articulos = '//th[@class="andes-table__header andes-table__header--left ui-pdp-specs__table__column ui-pdp-specs__table__column-title"]'
  else:
    path_articulos = '//th[@class="andes-table__header andes-table__header--left ui-vpp-striped-specs__row__column ui-vpp-striped-specs__row__column--id"]'

  ths = source.xpath(path_articulos)
  carac = [quitarAcentos(th.text_content()) for th in ths]
  tds = source.xpath('//span[@class="andes-table__column--value"]')
  valores = [td.text_content() for td in tds]
  a = {}
  for i in range(len(carac)):
    a[quitarAcentos(carac[i])] = quitarAcentos(valores[i])
  return a
  


def obtenerProductosDetallados(lis, wd):
    '''
    Recibe la lista de todos los articulos, y el webdriver y devuelve un
    dict con todos los resultados parseados
    '''
    page = []
        
    for li in lis:
        link    =  li.cssselect('a')[1].get('href')
        precio  =  li.cssselect('span.price-tag-fraction')[0].text_content()
        titulo  =  li.cssselect('h2.ui-search-item__title')[0].text_content()

        wd.get(link)
        source_code = html.fromstring(wd.page_source)

        features = obtenerFeatures(source_code)
        features["titulo"] = titulo
        features["Link"]   = link
        features["Precio"] = float(precio.replace('.', ''))
        
        page.append(features)
    return page


def getData(query):
    '''
    Recibe una palabra y busca la primer pagina de todos los productos de mercado libre de esa palabra,
    con todas sus especificaciones
    '''

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome = webdriver.Chrome('chromedriver',chrome_options=chrome_options)

    
    
    chrome.get("https://www.mercadolibre.com.ar/")

    check_box_wait = EC.presence_of_element_located((By.ID, 'cb1-edit'))
    WebDriverWait(chrome, 5).until(check_box_wait)

    inputBusqueda = chrome.find_element(By.ID, 'cb1-edit')
    inputBusqueda.send_keys(query)

    enter = chrome.find_element(By.CLASS_NAME,"nav-search-btn")
    enter.send_keys(Keys.ENTER)

    source_code = html.fromstring(chrome.page_source)
    lis = source_code.xpath('//li[@class="ui-search-layout__item"]')
    resultados = obtenerProductosDetallados(lis, chrome)
    
    # with open("data.json", "w") as f:
    #     json.dump(resultados, f)

    return jsonify(resultados)
