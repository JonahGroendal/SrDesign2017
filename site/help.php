<head>
    <?php
		include 'commonLinks.php';
		include 'header.php';
	?>
    <style type="text/css"><!-- .tab { margin-left: 40px; } --></style>
</head>
<body>
    <div class="page">
      <h1>Peptide Database</h1>
	  <h4>
	  Help/tutorial<br><br>
	  Introduction: A brief description of the database<br><br>
	  Browse: displays the database in a table and can be sorted by each column<br>
	  Hover over a column header to view description of each column<br>
	  Click the column header to sort by ascending/descending<br>
	  -1 indicates the activity is verified there<br>
	  -0 indicates activity is verified as not there<br>
	  -NA indicates no data on that activity for this peptide<br><br>


	  Search: Helps search for peptides based on:<br>
	  	<p>A. Sequence: enter a peptide sequence (letters only) to see if it is in the database</p>
	  	<p>B. Logical Operators: separates each search field</p>
            <p class="tab">1. OR: shows peptides that match any of the search criteria</p>
            <p class="tab">2. NOR: shows peptides that do not match any of the search criteria</p>
            <p class="tab">3. AND: shows peptides that match all of the search criteria</p>
	  	<p>C. Activity recorded: list of each activity in the database</p>
            <p class="tab">1. isTrue: peptide exhibits this activity</p>
            <p class="tab">2. isFalse: peptide confirmed does not exhibit this activity</p>
	</h4>
    </div>
</body>
