# Chat Multicast em Grupo com Criptografia AES-GCM

Aplicação de chat em rede local (LAN) desenvolvida em Python utilizando **sockets UDP Multicast** para comunicação em grupo e criptografia simétrica autenticada **AES-256-GCM** para proteção das mensagens.

## Funcionalidades

- **Comunicação em Grupo via Multicast (`224.1.1.1:5007`):** envio e recebimento simultâneo de mensagens entre múltiplos clientes na mesma rede local sem necessidade de um servidor central.
- **Concorrência com Threads:** escuta de pacotes em segundo plano (`threading`) enquanto o terminal permanece livre para digitação.
- **Criptografia Ponta a Ponta (AES-GCM):** derivação de chave de 256 bits via `SHA-256` a partir de uma senha pré-compartilhada, com geração de `nonce` aleatório de 12 bytes por mensagem. Pacotes enviados com chave divergente são detectados e descartados.

## Estrutura do Projeto

```text
├── docs/                # Capturas de tela e relatório técnico
├── src/
│   ├── __init__.py
│   ├── config.py        # Parâmetros de rede (IP multicast, porta, buffer e TTL)
│   ├── crypto.py        # Derivação de chave, cifragem e decifragem AES-GCM
│   ├── network.py       # Criação do socket UDP, entrada no grupo multicast e I/O
│   └── main.py          # Interface CLI e gerenciamento de threads
├── .gitignore
├── requirements.txt     # Dependências do projeto
└── README.md
```

## Instalação e Execução

1. **Clone o repositório:**
   ```bash
   git clone <URL_DO_SEU_REPOSITORIO>
   cd <NOME_DA_PASTA>
   ```

2. **Crie e ative um ambiente virtual (`venv`):**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
   *(No Windows, ative com: `venv\Scripts\activate`)*

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Execute o cliente:**
   ```bash
   python3 -m src.main
   ```

## Como Testar

1. Abra **3 terminais** na raiz do projeto (com o `venv` ativado) e execute `python3 -m src.main` em cada um.
2. Nos **Terminais 1 e 2**, informe nomes diferentes e a **mesma chave de sala** (ex: `redes2026`). As mensagens trocadas aparecerão decifradas em ambos.
3. No **Terminal 3**, informe uma **chave diferente** (ex: `senha_errada`). Ele receberá o datagrama UDP na rede, mas exibirá um alerta informando que a mensagem cifrada foi ignorada por falha na validação da chave.
4. Digite `/sair` para encerrar o cliente.

> **Nota sobre redes e firewall:** Em ambientes Linux com `ufw` ativo, libere a porta utilizada com `sudo ufw allow 5007/udp`. Em redes Wi-Fi institucionais com isolamento de clientes (*Client Isolation*), utilize um roteador local ou ponto de acesso (hotspot) para testar entre máquinas distintas.

## Demonstração

**Cliente 1 (chave correta):**
![Cliente 1](docs/cliente1.png)

**Cliente 2 (chave correta):**
![Cliente 2](docs/cliente2.png)

**Cliente 3 (chave incorreta — mensagem descartada):**
![Cliente 3 com chave incorreta](docs/intruso.png)

## Contexto Acadêmico

Projeto desenvolvido para a disciplina de **Redes de Computadores** do curso de **Bacharelado em Sistemas de Informação** — Universidade Federal de Uberlândia (UFU), Campus Monte Carmelo.
