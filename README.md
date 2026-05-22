# rssFeedReaderRPi 📰

Um leitor de feeds RSS leve, rápido e minimalista para terminal, desenvolvido especificamente para ser executado em **Raspberry Pi** rodando **Alpine Linux** (Alpine OS). 

O projeto foi projetado para consumir o mínimo possível de recursos de hardware, sendo perfeito para servidores domésticos, setups headless (sem interface gráfica) ou terminais SSH no Raspberry Pi.

---

## ✨ Funcionalidades

- 🗂️ **Organização por Categorias:** Navegação simples por categorias pré-configuradas de feeds RSS.
- 🎛️ **Interface de Terminal Interativa:** Menu simples numerado, ideal para navegação rápida pelo teclado.
- 🧹 **Leitura Limpa:** Remoção automática de tags HTML das descrições/conteúdos das notícias para melhor visualização no terminal.
- 📄 **Leitura Confortável:** Integração com o utilitário nativo `less` para permitir rolagem de texto (`scroll`), busca e leitura confortável das matérias completas.
- ⚡ **Ultra Leve:** Feito em Python puro, com pouquíssimas dependências e consumo de memória extremamente baixo.

---

## 🛠️ Requisitos do Sistema

- **Dispositivo:** Raspberry Pi (qualquer versão, desde o Pi Zero até o Pi 5).
- **Sistema Operacional:** Alpine Linux instalado.
- **Linguagem:** Python 3.x.
- **Utilitários:** `less` (preferencialmente a versão completa, em vez do minimalista integrado ao BusyBox).

---

## 🚀 Instalação e Configuração no Alpine OS

Como o Alpine Linux foca em segurança e leveza, e as versões modernas do Python adotam a especificação PEP 668 (que restringe a instalação global de pacotes via `pip`), você pode preparar o ambiente de duas maneiras.

Escolha a opção que melhor se adapta ao seu caso:

### Método 1: Instalação via Pacotes do Sistema (`apk`) — *Recomendado*
Esta é a melhor opção para o Raspberry Pi, pois utiliza pacotes pré-compilados pelo Alpine, poupando CPU e tempo de compilação.

1. **Atualize os repositórios:**
   ```bash
   apk update
   ```

2. **Instale as dependências essenciais do sistema:**
   ```bash
   apk add python3 py3-requests py3-feedparser less
   ```
   > 💡 **Nota:** O pacote `py3-feedparser` está no repositório `community` do Alpine. Caso receba um erro de pacote não encontrado, certifique-se de que o repositório `community` está ativado no seu arquivo `/etc/apk/repositories`.

---

### Método 2: Instalação via Ambiente Virtual Python (`venv`)
Caso prefira isolar as dependências ou o pacote `py3-feedparser` não esteja disponível na sua versão do Alpine:

1. **Instale o Python 3, Pip e o Less:**
   ```bash
   apk update
   ```
   ```bash
   apk add python3 py3-pip less
   ```

2. **Clone ou navegue até a pasta do projeto:**
   ```bash
   cd /home/ygorvieira/Projetos/rssFeedReaderRPi
   ```

3. **Crie e ative um ambiente virtual:**
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

4. **Instale as dependências via `pip`:**
   ```bash
   pip install requests feedparser
   ```

---

## 📖 Como Executar

Navegue até a pasta do projeto e execute o script principal:

### Se usou o Método 1 (Instalação Global via `apk`):
```bash
python3 jornalrss.py
```

### Se usou o Método 2 (Instalação via Ambiente Virtual):
```bash
source .venv/bin/activate
python3 jornalrss.py
```

---

## ⚙️ Personalização de Feeds

Para adicionar, remover ou modificar os feeds RSS do seu leitor, basta editar o dicionário no arquivo `feeds.py`.

```bash
nano feeds.py
```

O arquivo segue a seguinte estrutura:

```python
FEEDS = {
    "Nome da Categoria": {
        "Nome do Feed 1": "https://url-do-feed-1.com/rss",
        "Nome do Feed 2": "https://url-do-feed-2.com/feed"
    },
    "Outra Categoria": {
        "Nome do Feed 3": "https://url-do-feed-3.com/xml"
    }
}
```

Basta alterar os nomes e URLs para montar sua grade de notícias personalizada!

---

## ⌨️ Dicas de Navegação (no Leitor `less`)

Quando você abre uma notícia para leitura completa, ela é carregada utilizando o visualizador `less`. Use os seguintes comandos no teclado:

* **Seta para Baixo / Seta para Cima** ou **Espaço**: Rola o texto da notícia.
* **`q`**: Fecha a notícia e volta para o menu do leitor.
* **`/termo`**: Pesquisa por "termo" dentro da notícia.
* **`n`**: Vai para a próxima ocorrência do termo pesquisado.
