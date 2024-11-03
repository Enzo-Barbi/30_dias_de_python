
from typing import Literal, TypeAlias, get_args
import httpx
import respx

URL_COTACAO = 'https://economia.awesomeapi.com.br/json/last/{}'
Moeda: TypeAlias = Literal['EUR', 'USD', 'BTC']

def cotacao(moeda: Moeda):
    code = f'{moeda}-BRL'
    try:
        response = httpx.get(URL_COTACAO.format(code))
        data = response.json()[code.replace('-', '')]

        return f'Ultima cotacao: {data['high']}'
    except KeyError:
        return f'Codigo de moeda invalido. Use {get_args(Moeda)}'
    except UnicodeEncodeError:
        return f'Codigo de moeda invalido. Use {get_args(Moeda)}'
    except httpx.InvalidURL:
        return f'Codigo de moeda invalido. Use {get_args(Moeda)}'
    except httpx.ConnectError:
        return 'Erro de conexao, tente mais tarde'
    except httpx.TimeoutException:
        return 'Erro de conexao, tente mais tarde'

print(cotacao('USD'))

# Testes
@respx.mock
def teste_dolar():
    # Arange
    mocked_response = httpx.Response(
        200, json={'USDBRL': {'high': 5.8747}}
    )
    respx.get(
        URL_COTACAO.format('USD-BRL')
        ).mock(mocked_response)
    
    # Act
    result = cotacao('USD')

    # Assert
    assert result == 'Ultima cotacao: 5.8747'


def teste_moeda_errada():
    mocked_response = httpx.Response(
        200, json={}
    )
    respx.get(
        URL_COTACAO.format('MDT-BRL') #url da api porem com 'MDT-BRL' de param
        ).mock(mocked_response)

    result = cotacao('MDT')

    assert (
        result == "Codigo de moeda invalido. Use ('EUR', 'USD', 'BTC')"
    )


def teste_moeda_erro_na_URL():
    result = cotacao(r'\xwtzk11')

    assert (
        result == "Codigo de moeda invalido. Use ('EUR', 'USD', 'BTC')"
    )


@respx.mock
def teste_erro_conexao():
    #Arange
    respx.get(
        URL_COTACAO.format('USD-BRL')
        ).mock(side_effect=httpx.ConnectError)
    
    #Act
    result = cotacao('USD')

    #Assert
    assert result == 'Erro de conexao, tente mais tarde'


@respx.mock
def teste_erro_conexao():
    #Arange
    respx.get(
        URL_COTACAO.format('USD-BRL')
        ).mock(side_effect=httpx.TimeoutException)
    
    #Act
    result = cotacao('USD')

    #Assert
    assert result == 'Erro de conexao, tente mais tarde'

