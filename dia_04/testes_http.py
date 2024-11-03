from datetime import datetime
from typing import Literal, TypeAlias, get_args
import httpx
import respx
import humanize as h

h.activate('pt_BR')
URL_COTACAO = 'https://economia.awesomeapi.com.br/json/last/{}'
Moeda: TypeAlias = Literal['EUR', 'USD', 'BTC']
moedas = h.natural_list(get_args(Moeda)).replace('and', 'ou')

def cotacao(moeda: Moeda):
    code = f'{moeda}-BRL'
    try:
        response = httpx.get(URL_COTACAO.format(code))
        data = response.json()[code.replace('-', '')]
        isotime = datetime.fromtimestamp(
            int(data['timestamp']) 
        )
        return(
            f'Ultima cotacao ({h.naturaltime(isotime)}) : '  
            f'{h.intcomma(float(data['high']))}'
        ) 
    
    except KeyError:
        return f'Codigo de moeda ({moeda}) invalido. Use {moedas}'
    except UnicodeEncodeError:
        return f'Codigo de moeda invalido. Use {moedas}'
    except httpx.InvalidURL:
        return f'Codigo de moeda invalido. Use {moedas}'
    except httpx.ConnectError:
        return 'Erro de conexao, tente mais tarde'
    except httpx.TimeoutException:
        return 'Erro de conexao, tente mais tarde'

print(cotacao('EUR'))

# Testes
@respx.mock
def teste_dolar():
    # Arange
    mocked_response = httpx.Response(
        200, json={'USDBRL': {'high': 5.8747, 'timestamp': 0}}
    )
    respx.get(
        URL_COTACAO.format('USD-BRL')
        ).mock(mocked_response)
    
    # Act
    result = cotacao('USD')

    # Assert
    assert result == 'Ultima cotacao (há 54 anos) : 5,8747'


def teste_moeda_errada():
    mocked_response = httpx.Response(
        200, json={}
    )
    respx.get(
        URL_COTACAO.format('MDT-BRL') #url da api porem com 'MDT-BRL' de param
        ).mock(mocked_response)

    result = cotacao('MDT')

    assert (
        result == "Codigo de moeda (MDT) invalido. Use EUR, USD ou BTC"
    )


# def teste_moeda_erro_na_URL():
#     result = cotacao('\x01')

#     assert (
#         result == "Codigo de moeda () invalido. Use EUR, USD ou BTC"
#     )


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

