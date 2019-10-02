import re

import requests


URL = 'http://www.mtecbo.gov.br/cbosite/pages/pesquisas/BuscaPorCodigo.jsf'


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
