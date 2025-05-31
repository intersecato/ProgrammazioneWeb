<?php
require_once __DIR__ . '/../db.php';

header('Content-Type: application/json');

$input = json_decode(file_get_contents("php://input"), true);

if (
    !isset($input['codice']) || !is_numeric($input['codice']) ||
    !isset($input['titolo']) || !isset($input['anno']) ||
    !isset($input['durata']) || !isset($input['lingua'])
) {
    http_response_code(400);
    echo json_encode(["error" => "Dati mancanti o non validi"]);
    exit;
}

$codice = (int)$input['codice'];
$titolo = $conn->real_escape_string($input['titolo']);
$anno = (int)$input['anno'];
$durata = (int)$input['durata'];
$lingua = $conn->real_escape_string($input['lingua']);

$query = "UPDATE film SET titolo = ?, anno = ?, durata = ?, lingua = ? WHERE codice = ?";
$stmt = $conn->prepare($query);

if (!$stmt) {
    http_response_code(500);
    echo json_encode(["error" => "Errore nella preparazione della query: " . $conn->error]);
    exit;
}

$stmt->bind_param("siisi", $titolo, $anno, $durata, $lingua, $codice);

if ($stmt->execute()) {
    echo json_encode(["success" => true]);
} else {
    http_response_code(500);
    echo json_encode(["error" => "Errore durante l'aggiornamento: " . $stmt->error]);
}

$stmt->close();
$conn->close();
