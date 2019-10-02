import re

import requests


URL = 'http://www.mtecbo.gov.br/cbosite/pages/pesquisas/BuscaPorCodigo.jsf'


def get_javax_faces_viewstate(resp):
    view_state = re.search(
        r'id="javax.faces.ViewState" value="(-?\d+:\d+)"',
        resp.content.decode('latin-1')
    )
    return view_state.group(1)


def get_dtpinfra_token(resp):
    dtpinfra_token = re.search(
        r'name="DTPINFRA_TOKEN" value="(\d+)"',
        resp.content.decode('latin-1')
    )
    return dtpinfra_token.group(1)
