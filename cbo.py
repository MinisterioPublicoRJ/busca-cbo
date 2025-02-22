import re

import requests

from bs4 import BeautifulSoup


URL = 'http://www.mtecbo.gov.br/cbosite/pages/pesquisas/BuscaPorCodigo.jsf'


def simple_fifo_cache(cache_size):
    def inner_decorator(func):
        entries = dict()
        args_order = []

        def inner(cbo_code):
            cbo_code = format(cbo_code)
            if cbo_code in entries:
                return entries[cbo_code]

            resp = func(cbo_code)
            entries[cbo_code] = resp
            args_order.append(cbo_code)
            if len(args_order) == cache_size:
                entries.pop(args_order.pop(0))

            return resp

        return inner

    return inner_decorator


def get_javax_faces_viewstate(resp):
    view_state = re.search(
        r'id="javax.faces.ViewState" value="(-?\d+:-?\d+)"',
        resp.content.decode('latin-1')
    )
    return view_state.group(1)


def get_dtpinfra_token(resp):
    dtpinfra_token = re.search(
        r'name="DTPINFRA_TOKEN" value="(\d+)"',
        resp.content.decode('latin-1')
    )
    return dtpinfra_token.group(1)


def prepare_headers():
    headers = {
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36',
        'Origin': 'http://www.mtecbo.gov.br',
        'Content-Type': 'application/x-www-form-urlencoded',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Referer': 'http://www.mtecbo.gov.br/cbosite/pages/pesquisas/BuscaPorCodigo.jsf',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7',
    }

    return headers


def prepare_form_payload(session, cbo_code):
    headers = prepare_headers()
    resp = session.get(URL, headers=headers)
    data = {
      'formBuscaPorCodigo': 'formBuscaPorCodigo',
      'DTPINFRA_TOKEN': get_dtpinfra_token(resp),
      'formBuscaPorCodigo:j_idt84': cbo_code,
      'formBuscaPorCodigo:btConsultarCodigo': 'Consultar',
      'javax.faces.ViewState': get_javax_faces_viewstate(resp)
    }
    return data


def get_occupation(content):
    soup = BeautifulSoup(content, 'lxml')
    return soup.find('span', {'style': 'font-weight: bold'}).text


def format(cbo_code):
    code = re.sub(r'\D', '', cbo_code)
    return '{0}-{1}'.format(code[:5], code[5:])


@simple_fifo_cache(cache_size=50)
def search(cbo_code):
    session = requests.session()
    headers = prepare_headers()
    data = prepare_form_payload(session, cbo_code)
    resp = session.post(URL, data=data, headers=headers)
    occupation = get_occupation(resp.content)
    return occupation


if __name__ == "__main__":
    occupation = search('5211-25')
