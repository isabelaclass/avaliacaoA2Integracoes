# 🚨 Sistema de Integração de APIs para Monitoramento de Eventos Críticos

Este repositório apresenta uma solução de **integração de sistemas para monitoramento e resposta a eventos críticos**, utilizando múltiplas APIs desenvolvidas em diferentes linguagens e tecnologias. O projeto simula um cenário de **IoT e logística**, onde sensores disparam alertas que são processados e encaminhados para equipes de resposta.

---

## 🧱 Descrição

O projeto é composto por três APIs principais:

- **API Sensores (Node.js)**  
  Responsável por simular a coleta de dados de sensores (temperatura, pressão, etc.) e envio de alertas para eventos críticos.  
  Utiliza Redis para cache e integra com a API de eventos críticos.

- **API Eventos Críticos (Python/Flask)**  
  Recebe alertas dos sensores, armazena e disponibiliza eventos críticos.  
  Utiliza Redis para cache dos eventos e RabbitMQ para integração assíncrona com a API de logística.

- **API Logística (PHP)**  
  Gerencia equipamentos e despachos de recursos para resposta a eventos críticos.  
  Recebe comandos via RabbitMQ e expõe endpoints para consulta de equipamentos e envio de despachos.

---

## 🧰 Tecnologias Utilizadas

- Node.js (Express)  
- Python (Flask)  
- PHP (Composer, php-amqplib)  
- Redis (cache)  
- RabbitMQ (mensageria)

---

## 🚀 Como Executar

**Pré-requisitos:**

- Redis e RabbitMQ em execução  
- Cada API deve ser executada individualmente em seu ambiente correspondente

**Inicie cada API:**

```bash
# API Sensores (Node.js)
cd sensor-api
npm install
node index.js

# API Eventos Críticos (Python/Flask)
cd eventos-criticos-api
pip install -r requirements.txt
python app.py

# API Logística (PHP)
cd logistica-api
composer install
php -S localhost:8000 -t public
 ````

## ✅ Testes

Utilize ferramentas como **Postman** ou **cURL** para testar os endpoints das APIs.

---

## 🔌 Endpoints Principais

### 🔧 API Sensores

- `GET /sensor-data` — Retorna dados simulados de sensores  
- `POST /alert` — Envia alerta para a API de eventos críticos  

### ⚠️ API Eventos Críticos

- `POST /event` — Registra um novo evento crítico  
- `GET /events` — Lista eventos críticos registrados  

### 🚚 API Logística

- `GET /equipments` — Lista equipamentos disponíveis  
- `POST /dispatch` — Envia despacho para evento crítico  

---

Desenvolvido com 💙 por Isabela
