<?php
require_once __DIR__ . '/../db.php';

header('Content-Type: application/json');

$sql = "
    SELECT 
        s.numero,
        s.dim,
        s.tipo,
        COUNT(p.numProiezione) AS proiezioni
    FROM sala s
    LEFT JOIN proiezione p ON p.sala = s.numero
    GROUP BY s.numero
";

$result = $conn->query($sql);

if (!$result) {
    http_response_code(500);
    echo json_encode(["error" => "Errore nella query: " . $conn->error]);
    exit;
}

$sale = [];
while ($row = $result->fetch_assoc()) {
    $sale[] = [
        'numero'     => (int) $row['numero'],
        'dim'   => (int) $row['dim'],
        'tipo'       => $row['tipo'],
        'proiezioni' => (int) $row['proiezioni']
    ];
}

echo json_encode($sale, JSON_UNESCAPED_UNICODE);
$conn->close();
?>
