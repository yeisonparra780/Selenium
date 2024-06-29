from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import sys,os
from dotenv import load_dotenv
load_dotenv()
sys.path.append(os.getenv('RUTA_PROYECTO'))
import controladores.transacciones_oracle as to
# Configura el controlador de Chrome
# driver_path = 'path/to/chromedriver'


def llenar_formulario(codigo_respuesta,contrato,paquete,devolver_incapacidad,motivo_devolucion,lote):
    # Abre el formulario
    driver = webdriver.Chrome()
    url = 'https://forms.office.com/r/C0WUcKMj67'
    driver.get(url)
    current_url = driver.current_url
    print("URL actual:", current_url)
    # Espera a que la página se cargue completamente

    # Encuentra y llena los campos del formulario
    # Ajusta los selectores según sea necesario
    try:
        # wait = WebDriverWait(driver, 10)
        # empezar_ahora = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'css-178')))
        # Espera un máximo de 10 segundos a que aparezca el elemento
        time.sleep(10)

        try:
            driver.execute_script('document.querySelector(".css-161").click();')
        except:
            driver.execute_script('document.querySelector(".css-126").click();')
        time.sleep(5)
        driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div/div/div/div/div[3]/div/div/div[2]/div[2]/div[1]/div[2]/div/span/input").send_keys(codigo_respuesta)
        driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div/div/div/div/div[3]/div/div/div[2]/div[2]/div[2]/div[2]/div/span/input").send_keys(contrato)
        driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div/div/div/div/div[3]/div/div/div[2]/div[2]/div[3]/div[2]/div/span/input").send_keys(lote)
        driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div/div/div/div/div[3]/div/div/div[2]/div[2]/div[4]/div[2]/div/span/input").send_keys(paquete)

        if devolver_incapacidad == "1":
            driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div/div/div/div/div[3]/div/div/div[2]/div[2]/div[5]/div[2]/div/div/div[1]/div/label/span[1]").click()
            driver.find_element(By.XPATH,"/html/body/div[1]/div/div[1]/div/div/div/div/div[3]/div/div/div[2]/div[2]/div[6]/div[2]/div/div/div/span[1]").click()
            time.sleep(2)
            if motivo_devolucion == "Incompleta":
                driver.find_element(By.XPATH,"/html/body/div[2]/div/div[2]/span[2]/span").click()
            if motivo_devolucion == "Anterior ARL":
                driver.find_element(By.XPATH,"/html/body/div[2]/div/div[3]/span[2]/span").click()
            if motivo_devolucion == "Actual ARL":
                driver.find_element(By.XPATH,"/html/body/div[2]/div/div[4]/span[2]/span").click()
            if motivo_devolucion == "Sin salario":
                driver.find_element(By.XPATH,"/html/body/div[2]/div/div[5]/span[2]/span").click()
        else:
            driver.find_element(By.XPATH,"/html/body/div/div/div[1]/div/div/div/div/div[3]/div/div/div[2]/div[2]/div[5]/div[2]/div/div/div[2]/div/label/span[1]").click()
        # Añade más campos según sea necesario

        # Envía el formulario
        submit_button = driver.find_element(By.XPATH, '/html/body/div/div/div[1]/div/div/div/div/div[3]/div/div/div[2]/div[3]/div/button')
        submit_button.click()

        print('Formulario enviado con éxito')

    except Exception as e:
        print(f'Error al llenar el formulario: {e}')

    # Cierra el navegador
    time.sleep(2)
    driver.quit()
    

    
def main():

    lotes = to.buscar_lotes()
    if lotes:
        for lote in lotes:
            lot_id = lote[0]
            incapacidades = to.buscar_incapacidades(lot_id)
            for incapacidad in incapacidades:
                codigo_respuesta = incapacidad[0]
                contrato = incapacidad[1]
                lote = lot_id
                paquete = incapacidad[2]
                devolver_incapacidad = incapacidad[3]
                motivo_devolucion = incapacidad[4]
                print(incapacidad)
                llenar_formulario(codigo_respuesta,contrato,paquete,devolver_incapacidad,motivo_devolucion,lote)
                # to.actualizar_estado_lote(lot_id, 'completado')
    else:
        print('No hay lotes pendientes')


while True:
    if __name__ == "__main__":
        main()
        time.sleep(60)