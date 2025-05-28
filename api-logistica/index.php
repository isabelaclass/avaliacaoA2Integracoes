<?php

require_once __DIR__ . '/vendor/autoload.php';

use PhpAmqpLib\Connection\AMQPStreamConnection;
use PhpAmqpLib\Message\AMQPMessage;

header('Content-Type: application/json');

$method = $_SERVER['REQUEST_METHOD'];
$uri = strtok($_SERVER['REQUEST_URI'], '?');

// GET /equipments
if ($method === 'GET' && $uri === '/equipments') {
    echo json_encode([
        ["id" => 1, "name" => "Bomba Submersível", "status" => "disponível"],
        ["id" => 2, "name" => "Mangueira de Alta Pressão", "status" => "em uso"],
        ["id" => 3, "name" => "Gerador Portátil", "status" => "em manutenção"]
    ]);
    exit;
}

// POST /dispatch
if ($method === 'POST' && $uri === '/dispatch') {
    $body = file_get_contents('php://input');
    $data = json_decode($body, true);

    if (!$data) {
        http_response_code(400);
        echo json_encode(['error' => 'JSON inválido']);
        exit;
    }

    try {
        $connection = new AMQPStreamConnection('localhost', 5672, 'guest', 'guest');
        $channel = $connection->channel();

        $channel->queue_declare('critical-events', false, false, false, false);

        $msg = new AMQPMessage(json_encode($data));
        $channel->basic_publish($msg, '', 'critical-events');

        $channel->close();
        $connection->close();

        echo json_encode(['message' => 'Despacho enviado com sucesso.']);
    } catch (Exception $e) {
        http_response_code(500);
        echo json_encode(['error' => 'Erro ao enviar para o RabbitMQ: ' . $e->getMessage()]);
    }
    exit;
}

http_response_code(404);
echo json_encode(['error' => 'Rota não encontrada']);
