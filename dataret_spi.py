import requests
import pandas as pd
import datetime

def obter_token():
    url_token = "https://leituras.spi.engtecnologia.com/api/usuarios/login"
    
    # Informações de autenticação (pode variar de acordo com a API)
    credenciais = {
        "email_usuario": "",
        "senha": ""
    }

    # Requisição para obter o token
    resposta_token = requests.post(url_token, json=credenciais)
    resposta_token.raise_for_status()

    # Extrai o token de acesso do JSON da resposta
    token_acesso = resposta_token.json().get("token")
    return token_acesso

def requisitar_dados():
    # Obtém o token usando as credenciais
    token_acesso = obter_token()

    ########### POR EMPRESA
    # Use o token para fazer uma requisição à API
    url_api = "https://leituras.spi.engtecnologia.com/api/leituras/listar_leituras_por_idempresa"
    headers = {"Authorization": f"Bearer {token_acesso}"}

    try:
        resposta_api = requests.get(url_api, headers=headers)
        resposta_api.raise_for_status()

        dados = resposta_api.json()

        # Exporta os dados para um arquivo TXT
        with open("dados_api.txt", "w") as arquivo:
            arquivo.write(str(dados))
        
        # Imprime a resposta para visualização
        # print("Resposta da requisição à API:", resposta_api.text)

        return dados

    except requests.exceptions.HTTPError as errh:
        print(f"Erro HTTP: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Erro de Conexão: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Tempo Limite Expirado: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"Erro na requisição: {err}")

def processar_dados():
    dados_brutos = requisitar_dados()
    df = pd.DataFrame(dados_brutos['result'])
    df['valor_leitura'] = df['valor_leitura'].astype(float)
    df['data_leitura'] = pd.to_datetime(df['data_leitura'])
    mask = (df['data_leitura'] >= '2024-02-24')
    df = df.loc[mask]

    return df

def main():
    # Obtém os dados da API
    dados_api = processar_dados()

    # Exibe os dados
    # print(dados_api)

    # Salva os dados em um arquivo CSV
    # obtain the date
    hoje = datetime.datetime.now().strftime("%Y-%m-%d")
    dados_api.to_csv("~/hydronet/dados_sensores_updated_%s.csv" % hoje, index=False)
    dados_api.to_csv("~/hydronet/dados_sensores_updated.csv", index=False)
    print("Dados dos sensores de nível coletados e salvos com sucesso!")

if __name__ == "__main__":
    main()
    # print(dados_api)
