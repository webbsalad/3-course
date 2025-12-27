import os
import sys
from requests_oauthlib import OAuth2Session
from requests import HTTPError

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")

REDIRECT_URI = "http://localhost:8000/callback"


AUTHORIZATION_BASE_URL = "https://github.com/login/oauth/authorize"
TOKEN_URL = "https://github.com/login/oauth/access_token"


SCOPE = ["read:user", "user:email"]



if not CLIENT_ID or not CLIENT_SECRET:
    print("Ошибка: Переменные окружения CLIENT_ID и CLIENT_SECRET не установлены.")
    print("Пожалуйста, установите их перед запуском скрипта.")
    sys.exit(1)

def run_authorization_code_flow():
    """Реализует поток Authorization Code Flow."""
    print("--- Задание 1: Authorization Code Flow ---")

    try:

        oauth = OAuth2Session(CLIENT_ID, redirect_uri=REDIRECT_URI, scope=SCOPE)
        authorization_url, state = oauth.authorization_url(AUTHORIZATION_BASE_URL)
        
        print(f"\nПерейдите по ссылке для авторизации: \n{authorization_url}")
        print("\nПосле успешной авторизации, вас перенаправит на http://localhost:8000/callback?...")
        print("Скопируйте **полный URL** из адресной строки браузера и вставьте его ниже.")
        

        redirect_response = input("\nВставьте полный URL перенаправления: ")

        if not redirect_response.startswith(REDIRECT_URI):
            print("\nОшибка: Вставленный URL не начинается с ожидаемого REDIRECT_URI.")
            return


        print("\nОбмен кода авторизации на Access Token...")
        token = oauth.fetch_token(
            TOKEN_URL,
            authorization_response=redirect_response,
            client_secret=CLIENT_SECRET
        )
        
        print("\n✅ Access Token успешно получен.")
        print(f"Тип токена: {token.get('token_type')}")
        print(f"Срок действия (сек): {token.get('expires_in')}")

        print("\nДоступ к защищённому ресурсу (https://api.github.com/user)...")
        r = oauth.get("https://api.github.com/user")

        r.raise_for_status() 
        
        user_data = r.json()
        print("\n✅ Ответ от Resource Server:")
        print(f"Ваше имя: {user_data.get('name') or user_data.get('login')}")
        print(f"ID пользователя: {user_data.get('id')}")
        print(f"Публичных репозиториев: {user_data.get('public_repos')}")
        
        if 'refresh_token' in token:
            print("\n[ОПЦИОНАЛЬНО] Получен Refresh Token (для Задания 2):")
            print(f"Refresh Token: {token['refresh_token']}")
        
    except HTTPError as e:
        print(f"\n❌ Ошибка HTTP при обмене токена или запросе ресурса: {e}")
        print(f"Ответ сервера: {e.response.text}")
    except Exception as e:
        print(f"\n❌ Произошла непредвиденная ошибка: {e}")

if __name__ == "__main__":
    run_authorization_code_flow()