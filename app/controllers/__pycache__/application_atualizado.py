from bottle import template, redirect, request
from app.controllers.datarecord import DataRecord

class Application():

    def __init__(self):

        self.pages = {
            'index': self.index,
            'helper': self.helper,
            'pagina': self.pagina,
            'portal': self.portal
        }

        self.__model = DataRecord()
        self.__current_username = None # Corrigido para bater com o resto do código


    def render(self, page, parameter=None):
        """
        Renderiza uma página HTML do template
        
        Args:
            page (str): Nome da página ('index', 'helper', 'portal', 'pagina')
            parameter (str, optional): Parâmetro a passar para a função de página
        
        Returns:
            str: HTML renderizado
        """
        content = self.pages.get(page, self.helper)
        if not parameter:
            return content()
        else:
            return content(parameter)


    def get_session_id(self):
        """Obtém o ID de sessão do cookie"""
        return request.get_cookie('session_id')


    def index(self):
        """Renderiza a página inicial"""
        return template('app/views/html/index')


    def helper(self):
        """Renderiza a página de ajuda"""
        return template('app/views/html/helper')


    def portal(self):
        """Renderiza a página de login"""
        return template('app/views/html/portal')


    def pagina(self, parameter=None):
        """
        Renderiza a página de usuários com dados dinâmicos
        
        Args:
            parameter (str, optional): ID do usuário a exibir
        
        Returns:
            str: HTML renderizado com dados do usuário ou vazio
        """
        if not parameter:
            # Sem parâmetro: avisa o HTML que não há transferência
            return template('app/views/html/pagina', transfered=False)
        else:
            # Com parâmetro: busca o usuário no banco de dados usando self.__model
            info = self.__model.work_with_parameter(parameter)
            if not info:
                # Se digitar um ID que não existe, volta pra página inicial
                redirect('/pagina')
            else:
                # Se achou, avisa o HTML que teve transferência e envia os dados
                return template('app/views/html/pagina', transfered=True, data=info)


    def is_authenticated(self, username):
        """
        Verifica se um usuário está autenticado
        
        Args:
            username (str): Nome do usuário
        
        Returns:
            bool: True se autenticado, False caso contrário
        """
        session_id = self.get_session_id()
        current_username = self.__model.getUserName(session_id)
        return username == current_username


    def authenticate_user(self, username, password):
        """
        Autentica um usuário com username e password
        
        Args:
            username (str): Nome do usuário
            password (str): Senha do usuário
        
        Returns:
            tuple: (session_id, username) ou (None, None) se falhar
        """
        session_id = self.__model.checkUser(username, password)
        if session_id:
            self.logout_user()
            self.__current_username = self.__model.getUserName(session_id)
            return session_id, username
        return None, None


    def logout_user(self):
        """Faz logout do usuário atual"""
        self.__current_username = None
        session_id = self.get_session_id()
        if session_id:
            self.__model.logout(session_id)
