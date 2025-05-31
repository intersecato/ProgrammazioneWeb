<?php

ini_set('log_errors', 1);
ini_set('error_log', __DIR__ . '/../errors.log');
error_reporting(E_ALL);

$host = 'localhost';
$user = 'console';
$password = 'xs579zeQJd8FUNpVLmg62X';
$database = 'cinema';

$conn = new mysqli($host, $user, $password, $database);

if ($conn->connect_error) {
    error_log("Connessione fallita: " . $conn->connect_error);
    die("Connessione al database fallita.");
}

?>
