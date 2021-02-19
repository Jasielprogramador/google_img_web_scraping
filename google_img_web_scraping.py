# -*- coding: UTF-8 -*-   #para poder meter caracteres especiales
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import requests

uri = "https://www.google.com/search?q=pinarello+f12&rlz=1C1GCEU_esES852ES852&sxsrf=ACYBGNSC3GcurH4DwTMGQcWPle0C5SNibw:1572336121832&source=lnms&tbm=isch&sa=X&ved=0ahUKEwiAlInAgMHlAhWJnhQKHXOPD18Q_AUIEigB&biw=1920&bih=1040"
headers = {'Host': 'www.google.com',
           'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36"}
res = requests.get(uri, headers=headers, allow_redirects=False)
print(res.content)

# abrir el navegador
browser = webdriver.Firefox()
# abrir la pagina
browser.get(uri)
# esperar hasta que se haya renderizado el elemento que nos interesa (timeout=30s)

#como tal el nombre de la imagen tiene que tener un espacio pero este se reemplaza con un punto
WebDriverWait(browser, 30).until(EC.presence_of_all_elements_located((By.CLASS_NAME, "rg_i.Q4LuWd.Q4LuWd")))
# obtener el código HTML
html = browser.page_source
# cerrar el navegador
browser.close()

# instanciar un parser para html
# y cargar en memoria el DOM del html
# "soup" es una ref. al elemento raíz del DOM
soup = BeautifulSoup(html, 'html.parser')
# buscar en el DOM todos aquellos elementos
# cuyo atributo "class" valga "rg_i Q4LuWd tx8vtf"
img_results = soup.find_all('img', {'class': 'rg_i Q4LuWd tx8vtf'})
for idx, each in enumerate(img_results):
    src = ""
    if each.has_attr('src'):
        src = each['src']
    else:
        src = each['data-src']

    img_link = ""
    if src.find("data:image") != -1:
        img_link = each['data-iurl']
    else:
        img_link = src
    print(idx, img_link)

    res = requests.get(img_link)
    img = res.content
    file = open("./img/" + str(idx) + ".jpeg", "wb")
    file.write(img)
    file.close()


