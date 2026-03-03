# 📌 Requisitos do Sistema
Projeto: Controle Financeiro com IA integrada ao WhatsApp

---

## 1. Requisitos Funcionais

RF01 - O sistema deve permitir o cadastro de usuários.

RF02 - O sistema deve permitir autenticação por login e senha.

RF03 - O sistema deve permitir o registro manual de receitas.

RF04 - O sistema deve permitir o registro manual de despesas.

RF05 - O sistema deve permitir categorizar transações (ex: alimentação, transporte, investimento).

RF06 - O sistema deve permitir visualizar saldo total atualizado automaticamente.

RF07 - O sistema deve permitir visualizar histórico de transações.

RF08 - O sistema deve permitir cadastro de contas a pagar com data de vencimento.

RF09 - O sistema deve emitir alerta de contas próximas do vencimento.

RF10 - O sistema deve permitir integração com API para recebimento de mensagens via WhatsApp.

RF11 - O sistema deve processar mensagens em formato texto recebidas via API.

RF12 - O sistema deve processar áudios recebidos via API, convertendo para texto.

RF13 - O sistema deve processar imagens de comprovantes utilizando OCR.

RF14 - O sistema deve identificar automaticamente:
- Valor da transação
- Tipo (receita ou despesa)
- Data

RF15 - O sistema deve registrar automaticamente a transação identificada no banco de dados.

RF16 - O sistema deve gerar relatórios gráficos de despesas por categoria.

---

## 2. Requisitos Não Funcionais

RNF01 - O sistema deve possuir interface responsiva (desktop e mobile).

RNF02 - O sistema deve garantir autenticação segura de usuários.

RNF03 - O sistema deve armazenar dados financeiros de forma segura.

RNF04 - O sistema deve ser hospedado em ambiente de nuvem (Vercel ou similar).

RNF05 - O código deve ser versionado utilizando GitHub.

---

## 3. Regras de Negócio

RN01 - Transações classificadas como "despesa" devem reduzir o saldo total.

RN02 - Transações classificadas como "receita" devem aumentar o saldo total.

RN03 - Transações processadas automaticamente pela IA devem permitir confirmação pelo usuário antes do registro definitivo.

RN04 - Contas com vencimento próximo (até 3 dias) devem gerar alerta visual.

---

## 4. Escopo do Projeto

O sistema terá como foco principal a organização financeira pessoal, utilizando Inteligência Artificial para automatizar o registro de transações a partir de mensagens enviadas via WhatsApp.

Não faz parte do escopo:

- Consultoria financeira profissional.
- Integração direta com bancos.
- Operações financeiras reais (transferências ou pagamentos).
