from playwright.sync_api import Playwright, sync_playwright
from settings import logging, BASE_DIR
from pages.HomePage import HomePage
from utils.utils import read_excel
import os


def run(playwright: Playwright) -> None:    
    try:
        logging.info('Iniciando processo, abrindo navegador...')
        
        browser = playwright.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        
        logging.info(f'Navegador {browser.browser_type.name} iniciado')
        
        data_dir = os.path.join(BASE_DIR, 'data')
        if not os.path.exists(data_dir):
            os.mkdir(data_dir)
    
        home_page = HomePage(page)
        
        logging.info(f'Abrindo página {home_page.url}')
        
        home_page.open()
        
        logging.info('Fazendo download do arquivo...')
        
        download_info = home_page.download_file(data_dir)
        if download_info["error"]:
            logging.error(download_info["message"])
            return download_info
        
        full_path = download_info["data"]
        
        logging.info(f'Arquivo salvo em: {full_path}')
        
        data_file = read_excel(full_path)
        
        logging.info('Iniciando desafio...')
        
        start_challange = home_page.start_challange()
        if start_challange["error"]:
            logging.error(start_challange["message"])
            return start_challange
        
        data_to_form = home_page.send_data_to_form(data_file)
        if data_to_form["error"]:
            logging.error(data_to_form["message"])
            return data_to_form
            
        logging.info('Processo finalizado com sucesso')
        logging.info(f'Resultado: {data_to_form["data"]}')
        
    except Exception as e:
        logging.critical(f"Ocorreu um erro inesperado {e}")
    
    finally:
        context.close()
        browser.close()


if __name__ == "__main__":
    with sync_playwright() as playwright:
        run(playwright)
