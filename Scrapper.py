# %%
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from datetime import datetime
import pyodbc
import pandas as pd
from re import sub


# %%

options = Options()
options.add_argument('--headless')
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
datosBusqueda = dict(
    URL="https://www.cyberpuerta.mx/Computo-Hardware/Componentes/Tarjetas-de-Video/Filtro/Familia-de-procesadores-de-graficos/NVIDIA/Procesador-grafico/GeForce-RTX-4090/?ldtype=line&_artperpage=16",
    NombreProducto="emproduct_right_title",
    PrecioProducto="price",
    ClaseProductoIndividual="priceText"
)
urls = [
    "https://www.cyberpuerta.mx/Computo-Hardware/Componentes/Tarjetas-de-Video/Tarjeta-de-Video-ASUS-NVIDIA-GeForce-RTX-4090-ROG-Strix-24GB-384-Bit-GDDR6X-PCI-Express-4-0.html",
    "https://www.cyberpuerta.mx/Computo-Hardware/Componentes/Tarjetas-de-Video/Tarjeta-de-Video-ASUS-NVIDIA-ROG-Strix-GeForce-RTX-4090-OC-24GB-384-bit-GDDR6X-PCI-Express-4-0.html",
    "https://www.cyberpuerta.mx/Computo-Hardware/Componentes/Tarjetas-de-Video/Tarjeta-de-Video-Gigabyte-NVIDIA-GeForce-RTX-4090-GAMING-OC-24GB-384-bit-GDDR6X-PCI-Express-4-0.html",
    "https://www.cyberpuerta.mx/Computo-Hardware/Componentes/Tarjetas-de-Video/Tarjeta-de-Video-MSI-NVIDIA-GeForce-RTX-4090-GAMING-X-TRIO-24G-24GB-384-bit-GDDR6X-PCI-Express-4-0-cp2.html",
    "https://www.cyberpuerta.mx/Computo-Hardware/Componentes/Tarjetas-de-Video/Tarjeta-de-Video-MSI-NVIDIA-GeForce-RTX-4090-Gaming-X-Trio-24G-24GB-384-bit-GDDR6X-PCI-Express-4-0.html",
    "https://www.cyberpuerta.mx/Computo-Hardware/Componentes/Tarjetas-de-Video/Tarjeta-de-Video-MSI-NVIDIA-GeForce-RTX-4090-SUPRIM-LIQUID-X-24G-24GB-384-Bit-GDDR6X-PCI-Express-4-0.html",
    "https://www.cyberpuerta.mx/Computo-Hardware/Componentes/Tarjetas-de-Video/Tarjeta-de-Video-PNY-NVIDIA-GeForce-RTX-4090-24GB-OC-XLR8-Gaming-Verto-EPIC-X-RGB-TF-24GB-384-bit-GDDR6X-PCI-Express-x16-4-0.html",
    "https://www.cyberpuerta.mx/Computo-Hardware/Componentes/Tarjetas-de-Video/Tarjeta-de-Video-PNY-NVIDIA-GeForce-RTX-4090-TF-Verto-24GB-384-bits-GDDR6X-PCI-Express-x16-4-0.html",
    "https://www.cyberpuerta.mx/Computo-Hardware/Componentes/Tarjetas-de-Video/Tarjeta-de-Video-PNY-NVIDIA-GeForce-RTX-4090-XLR8-Gaming-Uprising-RGB-24GB-384-bit-GDDR6X-PCI-Express-x16-4-0.html",
    "https://www.cyberpuerta.mx/Computo-Hardware/Componentes/Tarjetas-de-Video/Tarjeta-de-Video-Zotac-NVIDIA-GeForce-RTX-4090-AMP-Extreme-AIRO-WHITE-24GB-384-bit-GDDR6X-PCI-Express-x16-4-0.html",
    "https://www.cyberpuerta.mx/Computo-Hardware/Componentes/Tarjetas-de-Video/Tarjeta-de-Video-Zotac-NVIDIA-GeForce-RTX-4090-Gaming-AMP-Extreme-AIRO-24GB-384-bit-GDDR6X-PCI-Express-x16-4-0.html",
    "https://www.cyberpuerta.mx/Computo-Hardware/Componentes/Tarjetas-de-Video/Tarjeta-de-Video-Zotac-NVIDIA-GeForce-RTX-4090-Gaming-Trinity-OC-24GB-384-bit-GDDR6X-PCI-Express-x16-4-0.html",
    "https://www.cyberpuerta.mx/Computo-Hardware/Componentes/Tarjetas-de-Video/Tarjeta-de-Video-Zotac-NVIDIA-GeForce-RTX-4090-Trinity-24GB-384-bit-GDDR6X-PCI-Express-x16-4-0.html"
]
cnxn = pyodbc.connect("Driver={SQL Server Native Client 11.0};"
                      "Server=localhost;"
                      "Database=nvidiaPriceAnalysis;"
                      "Trusted_Connection=yes;")
cursor = cnxn.cursor()
precio = []
print("La operacion comenzo a ejecutarse.." + str(datetime.now()))
for url in urls:
    driver.get(url)
    prices = driver.find_element(By.CLASS_NAME, datosBusqueda["ClaseProductoIndividual"])
    precio.append(int(float(sub(r'[^\d.]', '', prices.text))))
id = list(range(1, len(precio)+1))
data = pd.DataFrame(dict(Id=id, precio=precio, hora=datetime.now()))
for index, row in data.iterrows():
    cursor.execute("insert into precios ( precio, hora, Identificador) values(?,?,?)", row.precio, row.hora, row.Id,)
cnxn.commit()
cursor.close()

cnxn.close()
driver.close()
print("Operacion terminada con exito: " + str(datetime.now()))


#%%
