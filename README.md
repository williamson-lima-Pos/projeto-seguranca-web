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