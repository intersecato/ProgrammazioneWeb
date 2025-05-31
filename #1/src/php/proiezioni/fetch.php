<?php
require_once __DIR__ . '/../db.php';

header('Content-Type: application/json');

$sql = "
    SELECT 
        p.numProiezione,
        p.sala,
        p.data,
        p.ora,
        f.titolo AS film,
        COUNT(b.numProiezione) AS biglietti
    FROM proiezione p
    INNER JOIN film f ON p.filmProiettato = f.codice
    LEFT JOIN biglietto b ON b.numProiezione = p.numProiezione
    GROUP BY p.numProiezione, p.sala, p.data, p.ora, f.titolo
    ORDER BY p.data DESC, p.ora DESC
";

$result = $conn->query($sql);

if (!$result) {
    http_response_code(500);
    echo json_encode(["error" => "Errore nella query: " . $conn->error]);
    exit;
}

$proiezioni = [];
while ($row = $result->fetch_assoc()) {
    $proiezioni[] = [
        'numProiezione' => (int) $row['numProiezione'],
        'sala'          => $row['sala'],
        'data'          => $row['data'],
        'ora'           => $row['ora'],
        'film'          => $row['film'],
        'biglietti'     => (int) $row['biglietti']
    ];
}

echo json_encode($proiezioni, JSON_UNESCAPED_UNICODE);
$conn->close();
?>
