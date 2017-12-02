<?php
if (isset($_POST['seq'])) {
    $seq = $_POST['seq'];
}
else {
    $seq = "None";
}
if (isset($_POST['institution'])) {
    $inst = $_POST['institution'];
}
else {
    $inst = "None";
}
if (isset($_POST['activity'])) {
    $act = $_POST['activity'];
}
else {
    $act = "None";
}
?>
<head>
    <?php
		include 'commonLinks.php';
		include 'header.php';
	?>
</head>

<body>
	<div class="page">
		<h3><?php echo $seq; ?></h3>
        <h3><?php echo $inst; ?></h3>
        <h3><?php echo $act; ?></h3>
	</div>
