<?php
$connection = new MongoClient( "10.80.144.188" ); // connect to a remote host (default port: 27017)
// $db = $connection->selectDB("peptide");
$dbs = $connection->listDBs();
echo $dbs;

$connections = $connection->getConnections();

foreach ( $connections as $con )
{
    // Loop over all the connections, and when the type is "SECONDARY"
    // we close the connection
    if ( $con['connection']['connection_type_desc'] == "SECONDARY" )
    {
        echo "Closing '{$con['hash']}': ";
        $closed = $a->close( $con['hash'] );
        echo $closed ? "ok" : "failed", "\n";
    }
}
?>
?>
