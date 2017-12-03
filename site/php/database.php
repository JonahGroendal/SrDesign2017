<head>
    <?php
		include 'commonLinks.php';
		include 'header.php';
	?>
</head>

<body>
	<div class="tablepage">
		<a href="../res/db_dump.csv" download>Download Whole Database as CSV</a>
	</div>

	<script type="text/javascript" charset="utf-8">
	$(document).ready(function() {

        //Supressing warnings, there is a bug that i cant resolve. . .
        $.fn.dataTable.ext.errMode = 'none';

        $('#peptide_table').DataTable();
	} );
	</script>

	<div id="table_div" class="tablepage form-inline no-footer">
		<table id="peptide_table" class="table table-bordered">
		  <?php
		  	// echo '<script> document.getElementById("table_div").style.visibility = "hidden"; </script>';

			$myfile = fopen("../res/db_dump.csv", "r") or die("Unable to open file!");

			$line = fgets($myfile);
			$tokens = explode("|", $line);

			echo "<thead><tr>";

			$shrink_count = 0;

			for ($i = 0; $i < count($tokens); $i++)
			{
				if ($shrink_count < 3) //Change 3 to change the number of Columns keep their name
				{
					echo '<th>' . trim($tokens[$i]) . '</th>';
					$shrink_count++;
				}
				else
				{
					echo '<th id = "' .
					trim($tokens[$i]) .
					'" onmouseover="this.innerHTML=\'' .
					trim($tokens[$i]) .
					'\';" onmouseout="this.innerHTML=\'?\';" onclick="click_on(\'' .
					trim($tokens[$i]) .
					'\')">?</th>';
				}
			}

			echo "</tr></thead><tbody>";

			require '../vendor/autoload.php';

			$db = new MongoDB\Client("mongodb://localhost:27017");

			$collection = $db->peptide->peptide;
			$cursor = $collection->find(); // get all
			foreach ($cursor as $doc)
			{
				$array = iterator_to_array($doc);
				//Sequence
				echo "<tr><td>" . $array["sequence"] . "</td>";
				//Name
				echo "<td>NA</td>";
				//Type

				// $type = iterator_to_array($array["type"])["value"];
				if (iterator_to_array($array["type"])["value"])
				{
					echo "<td>" . iterator_to_array($array["type"])["value"] . "</td></tr>";
				}
				else
				{
					echo "<td>ZNA</td></tr>";
				}
				//Activities
				// echo "<td>" . $array[]

			}

			echo "</tbody>";

			fclose($myfile);

			// echo '<script> document.getElementById("table_div").style.visibility = "visible"; </script>';
		   ?>
		</table>
	</div>


</body>
