const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');
const redis = require('redis');
const dotenv = require('dotenv');

dotenv.config();

const app = express();
const PORT = 3000;
const REDIS_URL = 'redis://localhost:6379';
const ALERT_API_URL = 'http://localhost:5000/event';

app.use(bodyParser.json());

const redisClient = redis.createClient({ url: REDIS_URL });

redisClient.on('error', (err) => {
  console.error('Erro ao conectar ao Redis:', err);
});

redisClient.on('connect', () => {
  console.log('Conectado ao Redis com sucesso!');
});

(async () => {
  await redisClient.connect();
})();

// GET /sensor-data
app.get('/sensor-data', async (req, res) => {
  try {
    const cacheKey = 'sensor-data';
    const cachedData = await redisClient.get(cacheKey);

    if (cachedData) {
      return res.json(JSON.parse(cachedData));
    }

    const sensorData = {
      temperature: (Math.random() * 100).toFixed(2),
      pressure: (Math.random() * 200).toFixed(2),
    };

    await redisClient.setEx(cacheKey, 30, JSON.stringify(sensorData));

    res.json(sensorData);
  } catch (err) {
    console.error('Erro em /sensor-data:', err);
    res.status(500).json({ error: 'Erro ao obter dados do sensor.' });
  }
});

// POST /alert
app.post('/alert', async (req, res) => {
  try {
    const alertData = req.body;

    const response = await axios.post(ALERT_API_URL, alertData);
    res.json({ status: 'Alerta enviado com sucesso.', response: response.data });
  } catch (err) {
    console.error('Erro ao enviar alerta:', err);
    res.status(500).json({ error: 'Erro ao enviar alerta para a API Python.' });
  }
});

app.listen(PORT, () => {
  console.log(`API Sensores rodando em http://localhost:${PORT}`);
});
