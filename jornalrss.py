#!/us/bin/env python3

import os
import subprocess
import re

import feedparser
import requests
import tempfile

from datetime import datetime

from bs4 import BeautifulSoup

from feeds import FEEDS

def limpar_tela():
	os.system("clear")


def remover_html(texto):
	return re.sub(r"<[^>]+>", "", texto)

def carregar_feed(url):
	response = requests.get(
		url,
		headers={
			"User-Agent": "Mozilla/5.0 RSS Reader"
		},
		timeout=10
	)

	response.raise_for_status()

	return feedparser.parse(response.content)


def mostrar_categorias():
	while True:
		limpar_tela()

		categorias = list(FEEDS.keys())

		print("=" * 60)
		print(f"TECHJORNAL, edição de {datetime.now().strftime("%d-%m-%Y")} | Categorias")
		print("=" * 60)

		for i, categoria in enumerate(categorias, start=1):
			print(f"[{i}] {categoria}")

		print("\n[0] Sair")

		try:
			opcao = int(input("\nEscolha uma categoria: "))

			if opcao == 0:
				return None

			return categorias[opcao -1]

		except (ValueError, IndexError):
			pass


def mostrar_feeds(categoria):
	while True:
		limpar_tela()

		feeds = FEEDS[categoria]
		nomes = list(feeds.keys())

		print("\n" + "=" * 60)
		print(f"Feeds - {categoria}")
		print("=" * 60)

		for i, nome in enumerate(nomes, start=1):
			print(f"\n[{i}] {nome}")

		print("\n[0] Voltar")

		try:
			opcao = int(input("\nEscolha um feed: "))

			if opcao == 0:
				return None

			nome = nomes[opcao -1]

			return nome, feeds[nome]

		except (ValueError, IndexError):
			pass


def mostrar_noticias(nome_feed, url_feed):
    while True:
        limpar_tela()
        print("=" * 60)
        print(f"Carregando notícias de '{nome_feed}'...")
        print("=" * 60)

        try:
            feed = carregar_feed(url_feed)

        except requests.RequestException as erro:
            print("Erro ao carregar feed:\n")
            print(erro)

            input("\nENTER para voltar...")
            return

        except Exception as erro:
            print("Erro ao interpretar feed:\n")
            print(erro)

            input("\nENTER para voltar...")
            return

        if feed.bozo:
            print("Aviso ao interpretar feed:\n")
            print(feed.bozo_exception)

        if not feed.entries:
            print("Nenhuma notícia encontrada.")
            input("\nENTER para voltar...")
            return

        print("=" * 60)
        print(nome_feed)
        print("=" * 60)

        noticias = feed.entries[:10]

        for i, entry in enumerate(noticias, start=1):
            print(f"\n[{i}] {entry.title}")

            if hasattr(entry, "published"):
                print(f"Data: {entry.published}")

        print("\n[0] Voltar")

        try:
            opcao = int(input("\nEscolha uma notícia: "))

            if opcao == 0:
                return

            noticia = noticias[opcao - 1]

            ler_noticia(noticia)

        except (ValueError, IndexError) as erro:
            print(f"\nErro: {erro}")
            input("\nENTER para continuar...")	


def baixar_conteudo_original(url):
	try:
		response = requests.get(
			url,
			headers={
				"User-Agent": "Mozilla/5.0"
			},
			timeout=10
		)

		response.raise_for_status()

		soup = BeautifulSoup(response.text, "html.parser")

		paragrafos = soup.find_all("p")

		texto = "\n\n".join(
			p.get_text(strip=True)
			for p in paragrafos
			if p.get_text(strip=True)
		)

		return texto

	except Exception as erro:
		return f"Erro ao baixar conteúdo original:\n(erro)"



def obter_conteudo(entry):
	conteudo = ""

	if hasattr(entry, "content"):
		conteudo = "\n\n".join(
			remover_html(item.value)
			for item in entry.content
		)

	elif hasattr(entry, "summary"):
		conteudo = remover_html(entry.summary)

	elif hasattr(entry, "description"):
		conteudo = remover_html(entry.description)

	conteudo = conteudo.strip()

	#Se RSS trouxer pouco conteúdo,
	# tenta baixar do site original
	if len(conteudo) < 500:
		conteudo_site = baixar_conteudo_original(entry.link)

		if len(conteudo_site) > len(conteudo):
			return conteudo_site

	return conteudo


def ler_noticia(entry):
	limpar_tela()
	print("=" * 60)
	print("Carregando conteúdo da notícia...")
	print("=" * 60)
	
	conteudo = obter_conteudo(entry)

	texto = f"""
{entry.title}

{'=' * 60}

{conteudo}

{'=' * 60}

Link original:
{entry.link}
"""
	with tempfile.NamedTemporaryFile(
		mode="w",
		delete=False,
		encoding="utf-8"
	) as arquivo:

		arquivo.write(texto)
	
		caminho = arquivo.name

	subprocess.run(["less", caminho])
	
	os.remove(caminho)
	
def main():
	while True:
		categoria = mostrar_categorias()

		if categoria is None:
			break

		resultado = mostrar_feeds(categoria)

		if resultado is None:
			continue

		nome_feed, url_feed = resultado

		mostrar_noticias(nome_feed, url_feed)


if __name__ == "__main__":
	main()
