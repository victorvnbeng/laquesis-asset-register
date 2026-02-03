# Laquesis – Cadastro hierárquico de ativos a partir de Forms

Este projeto implementa um processo simples de ingestão de dados para cadastro de ativos de manutenção predial,
com geração automática de identificadores hierárquicos (ID) a partir de formulários preenchidos em campo.

O objetivo é apoiar a operação da Laquesis na organização dos ativos por empreendimento, ambiente e sistema,
com foco em uso futuro em análises técnicas

---

## Visão geral da solução

O fluxo é:

1. Técnico preenche um formulário padronizado em campo (ex: Microsoft Forms ou Google Forms)
2. As respostas são exportadas para um arquivo CSV
3. O script em Python importa o CSV
4. O banco de dados é alimentado automaticamente
5. O ID do ativo é gerado de forma hierárquica

Formato do identificador:

EE-AA-SS-QQQ


Onde:

- EE → sequência do empreendimento
- AA → sequência do ambiente dentro do empreendimento
- SS → sequência do sistema dentro do ambiente
- QQQ → sequência do equipamento dentro do sistema

Exemplo:

01-02-01-003


---

## Tecnologias utilizadas

- Python
- Pandas
- SQLite

---

## Estrutura do projeto

importar_forms_para_banco.py
README.md
.gitignore


---

## Estrutura mínima esperada do CSV

O arquivo CSV deve conter, no mínimo, as seguintes colunas:

- Empreendimento
- Ambiente
- Sistema
- Tipo do ativo
- Fabricante
- Modelo

---

## Observação importante

Os dados reais de clientes e operações não fazem parte deste repositório.
Os arquivos de banco de dados e planilhas de resposta são ignorados pelo `.gitignore`.

---

## Próximos passos planejados

- Geração de QR Code para cada ativo
- Integração futura com modelos BIM
- Evolução para banco em nuvem
- Painel de visualização dos ativos