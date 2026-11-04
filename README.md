# Projeto Segurança Web

**Repositório:** `projeto-seguranca-web`

## Autor e Contexto Acadêmico

**Autor:** Williamson Goulart Mendes de Lima  
**Curso:** Pós-Graduação em Segurança da Informação e Análise Forense  
**Projeto:** Projeto Final — Práticas de Mercado  

Este repositório integra o projeto final da Pós-Graduação em Segurança da
Informação e Análise Forense e tem como finalidade documentar e armazenar os
artefatos produzidos durante o desenvolvimento do projeto.

O projeto está organizado em eixos, contemplando infraestrutura em nuvem,
hospedagem e versionamento de código-fonte e desenvolvimento de uma aplicação
web com foco em práticas de segurança da informação.

## Descrição do Projeto

O Projeto Segurança Web consiste na implementação de uma infraestrutura em
nuvem e no desenvolvimento de uma aplicação web, aplicando controles e boas
práticas de Segurança da Informação durante todo o seu ciclo de construção.

O projeto contempla desde a preparação e proteção da infraestrutura de
hospedagem até o versionamento seguro do código-fonte e o desenvolvimento da
aplicação, incluindo mecanismos de autenticação, controle de acesso, proteção
de credenciais e tratamento seguro das informações.

## Autenticação SSH e Gerenciamento das Chaves

As operações de autenticação entre os ambientes locais de desenvolvimento e o
GitHub são realizadas por meio do protocolo SSH, utilizando chaves
criptográficas Ed25519.

Foi adotado um par de chaves SSH independente para cada equipamento utilizado
no desenvolvimento do projeto. Dessa forma, as chaves privadas não são
compartilhadas ou transferidas entre dispositivos.

Atualmente são utilizados dois ambientes de desenvolvimento:

- **Notebook de trabalho:** possui seu próprio par de chaves SSH Ed25519;
- **Computador pessoal:** possui outro par de chaves SSH Ed25519 independente.

As chaves privadas são mantidas exclusivamente nos respectivos dispositivos e
protegidas por passphrase. Somente as chaves públicas correspondentes foram
cadastradas na conta GitHub.

Essa estratégia permite que uma chave seja revogada individualmente em caso de
perda, comprometimento ou desativação de um equipamento, sem necessidade de
substituir as credenciais utilizadas nos demais dispositivos.

A autenticação SSH foi validada nos dois ambientes por meio de conexão com o
GitHub, confirmando o funcionamento das respectivas chaves.

## Proteção de Informações Sensíveis

Como o repositório do projeto é público, foram adotadas medidas para evitar o
versionamento e a publicação acidental de credenciais, chaves privadas, dados
locais e outros arquivos que possam representar risco de segurança.

O arquivo `.gitignore` foi configurado para impedir o versionamento de
categorias de arquivos que não devem ser armazenadas no repositório, incluindo:

- arquivos de variáveis de ambiente, como `.env`;
- ambientes virtuais Python, como `.venv/` e `venv/`;
- bancos de dados locais, como arquivos `.db`, `.sqlite` e `.sqlite3`;
- chaves privadas e certificados, incluindo arquivos `.pem`, `.key`, `.p12`
  e `.pfx`;
- chaves SSH privadas, como `id_rsa` e `id_ed25519`;
- arquivos relacionados a credenciais da Oracle Cloud Infrastructure;
- arquivos de log;
- arquivos temporários, caches e artefatos gerados pelo sistema operacional
  ou pelo editor.

O `.gitignore` atua de forma preventiva sobre arquivos ainda não versionados.
Ele não remove nem protege arquivos que já tenham sido adicionados ao histórico
do Git. Por esse motivo, credenciais, senhas, chaves privadas e outros segredos
não devem ser inseridos no repositório em nenhuma etapa do desenvolvimento.

Como camada adicional de proteção, o repositório utiliza os recursos
**Secret Scanning** e **Push Protection** do GitHub para auxiliar na detecção e
no bloqueio da publicação acidental de segredos.

## Itens do OWASP Top 10:2025 mitigados

- A01 — Broken Access Control
Controle de usuários, @login_required, @admin_required, permissões administrativas e proteção CSRF

- A02 — Security Misconfiguration
Hardening SSH, firewall, cabeçalhos HTTP, configurações por variáveis de ambiente e Fail2Ban

- A03 — Software Supply Chain Failures
Dependabot, monitoramento de dependências, requirements.txt e GitHub Actions

- A04 — Cryptographic Failures
Hash de senhas com scrypt, HTTPS/TLS e configuração de certificados

- A05 — Injection
SQLAlchemy ORM, consultas parametrizadas e testes contra SQL Injection

- A06 — Insecure Design
Separação de perfis, política de senhas, validação de entradas e proteção de sessões

- A07 — Authentication Failures
Login, logout, hash de senhas, validação de credenciais e gerenciamento de sessão

- A08 — Software or Data Integrity Failures
Versionamento Git, proteção do repositório e fluxo controlado de implantação

- A09 — Security Logging & Alerting Failures (parcial)
acesso seguro encriptografado. Não tem a função de alertas


