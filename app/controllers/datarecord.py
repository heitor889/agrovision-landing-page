from app.models.user_account import UserAccount
import json
import uuid


class DataRecord():
    """Banco de dados JSON para o recurso Usuários"""

    def __init__(self):

        self.__user_accounts= []
        self.__authenticated_users = {}
        self.read()


    def read(self):
        try:
            with open("app/controllers/db/user_accounts.json", "r") as arquivo_json:
                user_data = json.load(arquivo_json)
                self.__user_accounts = [UserAccount(**data) for data in user_data]
        except FileNotFoundError:
            self.__user_accounts.append(UserAccount('Guest', '010101','101010'))


    def book(self,username,password):

        new_user= UserAccount(username,password)
        self.__user_accounts.append(new_user)
        with open("app/controllers/db/user_accounts.json", "w") as arquivo_json:
            user_data = [vars(user_account) for user_account in \
            self.__user_accounts]
            json.dump(user_data, arquivo_json)


    def getCurrentUser(self,session_id):
        if session_id in self.__authenticated_users:
            return self.__authenticated_users[session_id]
        else:
            return None


    def getUserName(self,session_id):
        if session_id in self.__authenticated_users:
            return self.__authenticated_users[session_id].username
        else:
            return None


    def getUserSessionId(self, username):
        for session_id in self.__authenticated_users:
            if username == self.__authenticated_users[session_id].username:
                return session_id
        return None  # Retorna None se o usuário não for encontrado


    def checkUser(self, username, password):
        for user in self.__user_accounts:
            if user.username == username and user.password == password:
                session_id = str(uuid.uuid4())  # Gera um ID de sessão único
                self.__authenticated_users[session_id] = user
                return session_id  # Retorna o ID de sessão para o usuário
        return None


    def logout(self, session_id):
        if session_id in self.__authenticated_users:
            del self.__authenticated_users[session_id] # Remove o usuário logado

    def work_with_parameter(self, parameter):
        try:
            # Tenta converter o parâmetro da URL (ex: '0' ou '1') para um número inteiro
            index = int(parameter) 
            
            # Verifica se o índice existe na lista de usuários (para evitar dar erro se digitar /pagina/99)
            if 0 <= index < len(self.__user_accounts):
                return self.__user_accounts[index]
            else:
                return None
                
        except (ValueError, IndexError):
            # Se a conversão falhar (ex: digitou uma letra ao invés de número) ou o índice for inválido
            return None