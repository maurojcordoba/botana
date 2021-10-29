from bs4 import BeautifulSoup
import requests, re


def _partidos_url(cadena)->str:
    return fr'https://www.promiedos.com.ar/{cadena}'

def partidos_hoy(ligas):
    url = _partidos_url('hoy')
    return _partidos(url,ligas)

def partidos_ayer(ligas):
    url = _partidos_url('ayer')
    return _partidos(url,ligas)

def partidos_man(ligas):
    url = _partidos_url('man')
    return _partidos(url,ligas)

def _partidos(url,ligas) -> str:
    """devuelve un string con los partidos de las ligas 
    pasados por parametro - formato Markupdown"""

    result = ''

    #page = requests.get(url + "1",cookies=cookies_dict)
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser', multi_valued_attributes=None)

    # las ligas
    div_fixturein_list = soup.find_all('div', id='fixturein')
    
    for div in div_fixturein_list:        
        #recorrer las tr
        table = div.table

        liga = table.find('tr', class_='tituloin').text.strip()
        
        if (liga in ligas):
            result += f'*{liga}*\n'
            tr_list = table.find_all('tr', attrs={'name':re.compile('vp$')})

            for tr in tr_list:    
                #en_juego = tr['name']
                
                td_list = tr.find_all('td',attrs={'class':re.compile('^game')})    

                p = []
                for td in td_list:
                    p.append(td.text.strip())
                
                result += fr'{p[0]} - {p[1]} {p[2]} vs {p[3]} {p[4]}' + '\n'
            result+='\n'    

    return result
