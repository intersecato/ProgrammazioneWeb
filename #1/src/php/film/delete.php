<?php
require_once __DIR__ . '/../db.php';

header('Content-Type: application/json');

if ($_SERVER['REQUEST_METHOD'] === 'DELETE') {
    $id = (int)($_GET['id'] ?? 0);

    if ($id <= 0) {
        http_response_code(400);
        echo json_encode(['error' => 'ID non valido']);
        exit;
    }

    $stmt = $conn->prepare("DELETE FROM film WHERE codice = ?");
    if (!$stmt) {
        http_response_code(500);
        echo json_encode(['error' => 'Errore nella preparazione della query']);
        exit;
    }

    $stmt->bind_param("i", $id);
    $success = $stmt->execute();

    if ($success) {
        echo json_encode(['success' => true]);
    } else {
        http_response_code(500);
        echo json_encode(['error' => 'Errore durante l\'eliminazione']);
    }

    $stmt->close();
    $conn->close();
} else {
    http_response_code(405);
    echo json_encode(['error' => 'Metodo non consentito']);
}
