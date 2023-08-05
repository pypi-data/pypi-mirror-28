#!/usr/bin/env python
# -*- coding: utf-8 -*-
from cliente import BaseAPI


class Tribunais(BaseAPI):

    def __init__(self, token, url=BaseAPI.URL_DEFAULT):
        super(Tribunais, self).__init__(token, url)
        self.tribunais = None

    def _obtem_dados(self):
        resposta = self.executa_tribunal()
        self.valida_resposta(resposta)
        return resposta.json()

    def _numero_tribunal_por_sigla(self, sigla):
        # Retorna o número do tribunal
        for n, t in self.tribunais.items():
            if sigla.upper() == t['sigla'].upper():
                return n
        return None

    def obtem(self, tribunal):
        if not self.tribunais:
            self.tribunais = self._obtem_dados()
        n = self._numero_tribunal_por_sigla(tribunal) or tribunal
        t = self.tribunais.get(n, None)
        if t:
            return Tribunal(n, t)
        raise KeyError('Este parâmetro não consta como um tribunal válido')

    def completamente_suportado(self, tribunal):
        try:
            t = self.obtem(tribunal)
            if any([not s.suportado for s in t.sistemas]):
                return False
        except KeyError:
            return False
        return True

    def parcialmente_suportado(self, tribunal):
        t = self.obtem(tribunal)
        nenhum_suportado = all([not s.suportado for s in t.sistemas])
        todos_suportados = all([s.suportado for s in t.sistemas])
        if nenhum_suportado or todos_suportados:
            return False
        return True

    def por_estado(self, estado):
        if not self.tribunais:
            self.tribunais = self._obtem_dados()
        return [tr['sigla']
                for _, tr in self.tribunais.items()
                if estado.upper() in tr['estados']]


class Tribunal:

    def __init__(self, tribunal_numero, tribunal_info):
        self.numero = tribunal_numero
        self.sigla = tribunal_info['sigla']
        self.estados = tribunal_info['estados']
        self.nome = tribunal_info['nome']
        self.sistemas = []
        for sistema in tribunal_info['sistemas']:
            self.sistemas.append(SistemaTribunal(sistema))


class SistemaTribunal:

    def __init__(self, info):
        self.nome = info['nome']
        self.suportado = info['suportado']
        self.existe_busca_oab = info['existe_busca_oab']
        self.busca_oab_suportada = info['busca_oab_suportada']
