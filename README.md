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

## Objetivos

O objetivo geral do projeto é aplicar, em um ambiente prático, conhecimentos
adquiridos durante a Pós-Graduação em Segurança da Informação e Análise
Forense, integrando infraestrutura, desenvolvimento e segurança.

Entre os objetivos específicos estão:

- implementar uma infraestrutura em nuvem preparada para hospedar a aplicação;
- utilizar controle de versão e hospedagem segura do código-fonte;
- aplicar mecanismos para prevenir a exposição de credenciais e informações
  sensíveis no repositório;
- desenvolver uma aplicação web com autenticação e controle de acesso;
- aplicar práticas de desenvolvimento seguro durante a implementação;
- documentar as configurações, controles de segurança e procedimentos
  utilizados durante o projeto.

## Organização do Projeto

O projeto final está organizado em três eixos complementares, que representam
diferentes etapas da construção e proteção do ambiente.

### Eixo 1 — Infraestrutura

Responsável pela preparação da infraestrutura em nuvem destinada à hospedagem
da aplicação, incluindo a configuração e o endurecimento de segurança do
servidor, controle de acesso remoto, firewall, proteção do serviço web,
criptografia das comunicações, registros de eventos e demais controles de
infraestrutura.

### Eixo 2 — Hospedagem e Versionamento do Código-Fonte

Responsável pela hospedagem e pelo versionamento seguro do código-fonte no
GitHub, incluindo a configuração segura da conta e do repositório, autenticação
por chave SSH, proteção contra exposição de segredos e utilização adequada do
arquivo `.gitignore`.

Este repositório constitui o principal artefato deste eixo e será utilizado
também para armazenar os arquivos produzidos durante o desenvolvimento da
aplicação.

### Eixo 3 — Desenvolvimento da Aplicação

Responsável pelo desenvolvimento da aplicação web e pela implementação dos
controles de segurança relacionados ao software, incluindo autenticação,
controle de acesso, proteção de dados, validação das entradas e demais
mecanismos definidos para a aplicação.

`<ToDo>` { A documentação desta seção será complementada conforme os artefatos do Eixo 3 forem desenvolvidos e incorporados ao repositório.}

## Tecnologias e Ferramentas Utilizadas

As principais tecnologias e ferramentas utilizadas no projeto são:

- **Oracle Cloud Infrastructure (OCI):** plataforma de computação em nuvem
  utilizada para disponibilização da infraestrutura de hospedagem do projeto;

- **Git:** sistema de controle de versão distribuído utilizado para registrar e
  acompanhar as alterações realizadas nos arquivos do projeto;

- **GitHub:** plataforma utilizada para hospedagem do repositório remoto e
  gerenciamento do código-fonte;

- **SSH / Ed25519:** mecanismo utilizado para autenticação segura nas operações
  entre os ambientes locais de desenvolvimento e o GitHub;

- **Python 3.13:** linguagem e ambiente de execução selecionados para o
  desenvolvimento da aplicação;

- **Flask:** framework web Python selecionado para o desenvolvimento da
  aplicação;

- **pip:** gerenciador de pacotes utilizado para instalação e gerenciamento das
  dependências Python;

- **venv:** recurso utilizado para criação de um ambiente Python isolado para o
  projeto;

- **Sublime Text:** editor de código utilizado durante o desenvolvimento e
  manutenção dos arquivos do projeto.

## Segurança da Conta e do Repositório GitHub

A conta e o repositório utilizados no projeto foram configurados adotando
controles adicionais de segurança com o objetivo de reduzir os riscos de
acesso não autorizado, exposição de credenciais e inclusão de componentes
vulneráveis no código-fonte.

Entre os principais controles adotados estão:

- **Autenticação de dois fatores (2FA):** habilitada na conta GitHub por meio
  de aplicativo autenticador;

- **Códigos de recuperação:** gerados e armazenados separadamente para
  recuperação da conta em caso de indisponibilidade do segundo fator;

- **Privacidade do endereço de e-mail:** utilização do endereço `noreply`
  fornecido pelo GitHub para evitar a exposição do endereço de e-mail pessoal
  nos commits;

- **Proteção contra exposição do e-mail:** habilitado o bloqueio de operações
  de linha de comando que possam publicar o endereço de e-mail privado;

- **Secret Scanning:** habilitado para auxiliar na identificação de credenciais
  e outros segredos eventualmente incluídos no repositório;

- **Push Protection:** habilitado para auxiliar no bloqueio da publicação de
  segredos detectados durante operações de push;

- **Dependency Graph:** habilitado para permitir a identificação das
  dependências utilizadas pelo projeto;

- **Dependabot Alerts:** habilitado para geração de alertas relacionados a
  vulnerabilidades conhecidas nas dependências;

- **Dependabot Security Updates:** habilitado para auxiliar na atualização de
  dependências que apresentem vulnerabilidades conhecidas;

- **Dependabot Malware Alerts:** habilitado para auxiliar na identificação de
  pacotes associados a ameaças ou comportamento malicioso.

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

## Ambiente Python e Gerenciamento de Dependências

O desenvolvimento da aplicação utiliza **Python 3.13** e um ambiente virtual
Python (`venv`) para isolar as dependências do projeto das demais instalações
existentes no sistema operacional.

O diretório `.venv/` não é armazenado no repositório, pois contém arquivos
específicos do ambiente local e pode ser reconstruído quando necessário.

As dependências Python utilizadas pelo projeto são registradas no arquivo
`requirements.txt`, permitindo que o ambiente seja reproduzido em outro
equipamento sem a necessidade de versionar o ambiente virtual.

A reprodutibilidade foi validada utilizando dois ambientes independentes. O
repositório foi clonado em outro computador, uma nova `.venv` foi criada
localmente e as dependências foram instaladas a partir do `requirements.txt`.

Para instalar as dependências em um ambiente virtual previamente criado e
ativado, utiliza-se:

    python -m pip install -r requirements.txt

Esse procedimento confirmou a instalação das mesmas dependências registradas
no projeto, incluindo o **Flask 3.1.3**, demonstrando que o ambiente de
desenvolvimento pode ser reconstruído a partir dos arquivos versionados no
repositório.

## Obtenção e Preparação do Projeto

O código-fonte é mantido em um repositório público no GitHub e pode ser
obtido utilizando o Git por meio de conexão HTTPS ou SSH.

Nos ambientes utilizados durante o desenvolvimento, foi adotada a autenticação
por SSH.

Após o clone do repositório, o ambiente local pode ser preparado com a criação
de um ambiente virtual Python e a instalação das dependências registradas no
projeto.

Exemplo de preparação utilizando PowerShell:

    git clone git@github.com:williamson-lima-Pos/projeto-seguranca-web.git
    cd projeto-seguranca-web
    python -m venv .venv
    .\.venv\Scripts\Activate.ps1
    python -m pip install -r requirements.txt

A ativação do ambiente virtual pode depender da política de execução de scripts
configurada no PowerShell. Essa política deve ser avaliada conforme as regras
de segurança do equipamento utilizado.

As credenciais e configurações sensíveis necessárias à execução da aplicação
não deverão ser armazenadas diretamente no código-fonte ou no repositório.