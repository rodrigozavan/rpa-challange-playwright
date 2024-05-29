from playwright.sync_api import Page, expect
from typing import List
import os

class HomePage:
    """
    Classe que representa a página inicial do desafio RPA.
    """

    def __init__(self, page: Page):
        """
        Inicializa a página inicial do desafio RPA.

        Args:
            page (Page): A página do Playwright.
        """
        self.page = page
        self.__url = 'https://rpachallenge.com/'
        
    @property
    def url(self):
        """
        Obtém a URL da página inicial.

        Returns:
            str: A URL da página inicial.
        """
        return self.__url
    
    @url.setter
    def url(self, value):
        """
        Define a URL da página inicial.

        Args:
            value (str): A URL da página inicial.
        """
        self.__url = value

    def open(self, timeout=60000):
        """
        Abre a página inicial do desafio RPA.

        Args:
            timeout (int, optional): O tempo máximo de espera em milissegundos. Defaults to 60000.
        """
        self.page.goto(
            url=self.url,
            wait_until='domcontentloaded',
            timeout=timeout
        )
        
    def download_file(self, path_to_save:str, timeout:int=60000):
        """
        Faz o download do arquivo Excel.

        Args:
            path_to_save (str): O caminho onde o arquivo será salvo.
            timeout (int, optional): O tempo máximo de espera em milissegundos. Defaults to 60000.

        Returns:
            dict: Um dicionário contendo informações sobre o download.
                - error (bool): Indica se ocorreu algum erro durante o download.
                - message (str): A mensagem de erro ou sucesso.
                - data (str): O caminho completo do arquivo salvo.
        """
        try:
            download_button = self.page.get_by_role(
                "link", 
                name="Download Excel cloud_download"
            )
            
            expect(download_button).to_be_visible(timeout=timeout)
            
            with self.page.expect_download() as download_info:
                download_button.click()
            
            download = download_info.value
            
            full_path = os.path.join(path_to_save, download.suggested_filename)
            
            download.save_as(path=full_path)
            
        except Exception as e:
            return {
                'error': True,
                'message': f'Erro ao tentar fazer download do arquivo: {e}',
                'data': None
            }

        return {
            'error': False,
            'message': 'Download realizado com sucesso',
            'data': full_path
        }
    
    def start_challange(self, timeout:int=60000):
        """
        Inicia o desafio RPA.

        Args:
            timeout (int, optional): O tempo máximo de espera em milissegundos. Defaults to 60000.

        Returns:
            dict: Um dicionário contendo informações sobre o início do desafio.
                - error (bool): Indica se ocorreu algum erro durante o início do desafio.
                - message (str): A mensagem de erro ou sucesso.
                - data (None): Sem dados adicionais.
        """
        try:
            submit_button = self.page.get_by_role(
                "button", 
                name="Start"
            )
            
            expect(submit_button).to_be_visible(timeout=timeout)
            
            submit_button.click()
            
        except Exception as e:
            return {
                'error': True,
                'message': f'Erro ao tentar iniciar o desafio: {e}',
                'data': None
            }
        
        return {
            'error': False,
            'message': 'Desafio iniciado com sucesso',
            'data': None
        }
    
    def send_data_to_form(self, data:List[dict], timeout:int=60000):
        """
        Envia os dados para o formulário do desafio RPA.

        Args:
            data (List[dict]): Uma lista de dicionários contendo os dados a serem enviados.
            timeout (int, optional): O tempo máximo de espera em milissegundos. Defaults to 60000.

        Returns:
            dict: Um dicionário contendo informações sobre o envio dos dados.
                - error (bool): Indica se ocorreu algum erro durante o envio dos dados.
                - message (str): A mensagem de erro ou sucesso.
                - data (str): O resultado da submissão do formulário.
        """
        try:
            for item in data:
                for key, value in item.items():
                    input_field = self.page.locator("rpa1-field").filter(has_text=key)
                
                    expect(input_field).to_be_visible(timeout=timeout)
                    
                    input_field.locator("input").fill(str(value))
                    
                submit_button = self.page.get_by_role(
                    "button", 
                    name="Submit"
                )
                
                expect(submit_button).to_be_visible(timeout=timeout)
                
                submit_button.click()
            
            result = self.page.locator(".message2").text_content()

        except Exception as e:
            return {
                'error': True,
                'message': f'Erro ao tentar enviar os dados para o formulário: {e}',
                'data': None
            }
        
        return {
            'error': False,
            'message': 'Dados enviados com sucesso',
            'data': result
        }
