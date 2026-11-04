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

### A01 — Broken Access Control - Controle de usuários, @login_required, @admin_required, permissões administrativas e proteção CSRF

A aplicação implementa controle de acesso baseado em perfis (RBAC — Role-Based Access Control), distinguindo usuários comuns e administradores por meio do atributo is_admin, definido no arquivo app.py, linha 73.

A autenticação e a autorização são verificadas no servidor por meio dos decoradores login_required (app.py, linhas 148–158) e admin_required (app.py, linhas 161–184). O acesso administrativo é condicionado à existência de uma sessão autenticada e à confirmação do privilégio administrativo, sendo negado aos usuários comuns por meio da resposta HTTP 403 (Forbidden).

As rotas de administração e gerenciamento de privilégios são protegidas pelo decorador @admin_required, conforme demonstrado nas linhas 342–343, 355–356 e 391–392 do arquivo app.py.

Adicionalmente, novos usuários são cadastrados sem privilégios administrativos, conforme as linhas 244–245 do arquivo app.py, mitigando a atribuição indevida de permissões elevadas.

### A02 — Security Misconfiguration - Hardening SSH, firewall, cabeçalhos HTTP, configurações por variáveis de ambiente e Fail2Ban

A aplicação e sua infraestrutura incorporam medidas de configuração segura destinadas à redução da superfície de ataque e à mitigação de configurações inadequadas.

No código-fonte, arquivo app.py, destacam-se a configuração de atributos de segurança dos cookies de sessão (linhas 26–34), a definição do tempo de expiração das sessões permanentes (linhas 36–37) e a aplicação de cabeçalhos HTTP de segurança (linhas 187–193). Também foram implementados mecanismos de carregamento da chave secreta por variável de ambiente (linhas 14–18) e controle do modo de depuração (linhas 440–443).

Na infraestrutura, foram configurados mecanismos de filtragem de tráfego de rede, restrições de autenticação SSH, proteção contra tentativas repetidas de acesso, desativação de serviços desnecessários e comunicação HTTPS por meio do Nginx.

### A04 — Cryptographic Failures - Hash de senhas com scrypt, HTTPS/TLS e configuração de certificados

A aplicação implementa mecanismos de proteção criptográfica para senhas de usuários, utilizando as funções generate_password_hash e check_password_hash, disponibilizadas pela biblioteca Werkzeug.

No arquivo app.py, o método set_password (linhas 118–123) realiza a validação da senha e gera seu hash antes do armazenamento. O método check_password (linhas 125–129) verifica as credenciais durante a autenticação, comparando a senha fornecida com o hash previamente armazenado. No ambiente de produção, foi identificado o uso do algoritmo scrypt.

Na infraestrutura, a aplicação utiliza HTTPS com certificados digitais emitidos pela Let's Encrypt e gerenciamento de renovação por meio do Certbot. Também foi configurado um script para validar a configuração do Nginx antes de sua recarga após a renovação bem-sucedida do certificado.

Essas medidas contribuem para proteger as credenciais armazenadas e a confidencialidade e integridade dos dados transmitidos entre o navegador e o servidor.

### A05 — Injection - SQLAlchemy ORM, consultas parametrizadas e testes contra SQL Injection

A aplicação implementa mecanismos de mitigação contra ataques de SQL Injection por meio da utilização do SQLAlchemy ORM (Object-Relational Mapping), responsável pela interação com o banco de dados SQLite.

No arquivo app.py, as consultas realizadas durante o cadastro de usuários (linhas 235–238) e a autenticação (linhas 290–293) utilizam a construção db.select(User).filter_by(username=username), permitindo que os valores fornecidos pelos usuários sejam tratados como parâmetros, sem concatenação direta em instruções SQL.

O mesmo padrão de acesso ao banco de dados é utilizado nas funcionalidades administrativas, incluindo a listagem de usuários (app.py, linhas 348–350), a promoção de privilégios (app.py, linhas 365–366) e sua revogação (app.py, linhas 401–402).

Adicionalmente, a aplicação possui mecanismos de validação de entradas, contribuindo para restringir dados inválidos e reduzir riscos associados ao processamento de informações fornecidas pelos usuários.

Essas medidas mitigam o risco de SQL Injection nas operações identificadas, embora não substituam a necessidade de testes de segurança e revisão de eventuais consultas SQL executadas diretamente.

### A06 — Insecure Design - Separação de perfis, política de senhas, validação de entradas e proteção de sessões

O projeto incorporou princípios de segurança desde sua implementação, destacando-se a separação de responsabilidades, a atribuição de privilégios mínimos e a adoção de políticas de autenticação e autorização.

Na aplicação Flask, o controle de acesso baseado em perfis é implementado por meio do atributo is_admin (app.py, linha 73), dos mecanismos de autenticação e autorização (app.py, linhas 135–184) e da atribuição de privilégios comuns aos novos usuários (app.py, linhas 244–245).

Também foram implementadas validações de credenciais e mecanismos de gerenciamento de sessões, incluindo a definição de tempo de expiração de 30 minutos para sessões permanentes (app.py, linhas 36–37).

Na infraestrutura Ubuntu, foram estabelecidas contas distintas para administração e atividades de desenvolvimento, além de uma identidade específica para execução do serviço da aplicação, contribuindo para a segregação de responsabilidades.

### A07 — Authentication Failures - Login, logout, hash de senhas, validação de credenciais e gerenciamento de sessão (Parcial)

A aplicação Flask implementa mecanismos de autenticação e proteção de credenciais, incluindo política de validação de senhas, geração de hashes com o algoritmo scrypt e verificação das credenciais fornecidas pelos usuários.

No arquivo app.py, destacam-se os métodos de geração e verificação dos hashes de senha (linhas 118–129), a validação de credenciais durante o login (linhas 290–300), a limpeza da sessão anterior à autenticação (linha 303) e o armazenamento do identificador do usuário na sessão (linha 309).

Também foram implementados mecanismos de proteção de cookies no arquivo app.py, incluindo os atributos HttpOnly (linha 28), SameSite=Lax (linha 31) e configuração condicional de Secure (linha 34). As sessões permanentes possuem tempo de expiração configurado em 30 minutos (linha 37), e o encerramento da sessão é realizado pela funcionalidade de logout (linhas 320–332).

Entretanto, a aplicação ainda não possui implementação comprovada de autenticação multifator, limitação de tentativas de login ou mecanismos específicos de proteção contra ataques de força bruta e credential stuffing.

Dessa forma, o A07 é classificado como parcialmente implementado, com controles efetivos no código-fonte e oportunidades de aprimoramento na proteção contra ataques automatizados às credenciais.

### A09 — Security Logging & Alerting Failures (parcial) - acesso seguro encriptografado. Não tem a função de alertas

autenticação segura por login e senha, no arquivo app.py nas linhas 125–129, 290–312 e 335–339


