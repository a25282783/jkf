<?php
$pdo = new Simplon\Mysql\PDOConnector(
    'localhost',
    'root',
    '',
    'jkf'
);

$pdoConn = $pdo->connect('utf8', []); // charset, options

$dbConn = new Simplon\Mysql\Mysql($pdoConn);
