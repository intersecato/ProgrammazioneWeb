<?php
require_once __DIR__ . '/../db.php';

header('Content-Type: application/json');

$input = json_decode(file_get_contents('php://input'), true);

if (!$input || !isset($input['titolo'], $input['anno'], $input['durata'], $input['lingua'])) {
    http_response_code(400);
    echo json_encode(['error' => 'Dati non validi']);
    exit;
}

$titolo = trim($input['titolo']);
$anno = (int)$input['anno'];
$durata = (int)$input['durata'];
$lingua = trim($input['lingua']);

$query = "INSERT INTO film (titolo, anno, durata, lingua) VALUES (?, ?, ?, ?)";
$stmt = $conn->prepare($query);

if ($stmt === false) {
    http_response_code(500);
    echo json_encode(['error' => 'Errore nella preparazione della query']);
    exit;
}

$stmt->bind_param("siis", $titolo, $anno, $durata, $lingua);

if ($stmt->execute()) {
    http_response_code(200);
    echo json_encode(['success' => true]);
} else {
    http_response_code(500);
    echo json_encode(['error' => 'Errore nell\'esecuzione della query']);
}

$stmt->close();
$conn->close();
