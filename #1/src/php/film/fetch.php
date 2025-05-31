<?php
require_once __DIR__ . '/../db.php';

header('Content-Type: application/json');

$titolo = isset($_GET['titolo']) ? $conn->real_escape_string($_GET['titolo']) : '';

$sql = "
    SELECT 
        f.codice,
        f.titolo,
        f.anno,
        f.durata,
        f.lingua,
        COUNT(DISTINCT p.numProiezione) AS proiezioni,
        COUNT(b.numProiezione) AS vendite
    FROM film f
    LEFT JOIN proiezione p ON p.filmProiettato = f.codice
    LEFT JOIN biglietto b ON b.numProiezione = p.numProiezione
";

if (!empty($titolo)) {
    $sql .= " WHERE f.titolo LIKE '%$titolo%'";
}

$sql .= " GROUP BY f.codice";

$result = $conn->query($sql);

if (!$result) {
    http_response_code(500);
    echo json_encode(["error" => "Errore nella query: " . $conn->error]);
    exit;
}

$film = [];
while ($row = $result->fetch_assoc()) {
    $film[] = [
        'codice'      => (int) $row['codice'],
        'titolo'      => $row['titolo'],
        'anno'        => (int) $row['anno'],
        'durata'      => (int) $row['durata'],
        'lingua'      => $row['lingua'],
        'proiezioni'  => (int) $row['proiezioni'],
        'vendite'     => (int) $row['vendite']
    ];
}

echo json_encode($film, JSON_UNESCAPED_UNICODE);
$conn->close();
?>