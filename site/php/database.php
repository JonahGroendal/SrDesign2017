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
          // phpinfo();
            // require '../vendor/autoload.php';
            //
            // $db = new MongoDB\Client("peptide://localhost:27017");
            //
            // // select a collection (analogous to a relational database's table)
            // $collection = $db->peptide;
            //
			// // find everything in the collection
			// $cursor = $collection->find();

		  	echo '<script> document.getElementById("table_div").style.visibility = "hidden"; </script>';

			$myfile = fopen("../res/db_dump.csv", "r") or die("Unable to open file!");

			$line = fgets($myfile);
			$tokens = explode("|", $line);

			echo "<thead><tr>";

			$shrink_count = 0;

			// for ($i = 0; $i < count($tokens); $i++)
			// {
			// 	if ($shrink_count < 3) //Change 3 to change the number of Columns keep their name
			// 	{
			// 		echo '<th>' . trim($tokens[$i]) . '</th>';
			// 		$shrink_count++;
			// 	}
			// 	else
			// 	{
			// 		echo '<th id = "' .
			// 		trim($tokens[$i]) .
			// 		'" onmouseover="this.innerHTML=\'' .
			// 		trim($tokens[$i]) .
			// 		'\';" onmouseout="this.innerHTML=\'?\';" onclick="click_on(\'' .
			// 		trim($tokens[$i]) .
			// 		'\')">?</th>';
			// 	}
			// }
            foreach ($cursor as $document)
            {
                foreach ($document as $attribute)
                {
                    if ($shrink_count < 3) //Change 3 to change the number of Columns keep their name
        				{
        					echo '<th>' . $attribute . '</th>';
        					$shrink_count++;
        				}
        				else
        				{
        					echo '<th id = "' .
        					$attribute .
        					'" onmouseover="this.innerHTML=\'' .
        					$attribute .
        					'\';" onmouseout="this.innerHTML=\'?\';" onclick="click_on(\'' .
        					$attribute .
        					'\')">?</th>';
        				}
                }
            }

			echo "</tr></thead><tbody>";

			while (!feof($myfile))
			{
				$line = fgets($myfile);
				$tokens = explode("|", $line);


				if (strlen(trim($tokens[0])) < 50)
				{
					echo "<tr>";
					for ($i = 0; $i < count($tokens); $i++)
					{
						if (trim($tokens[$i]) === "None")
						{
								$tokens[$i] = "NA";
						}
						echo "<td>" . trim($tokens[$i]) . "</td>";
					}
					echo "</tr>";
				}
			}

			echo "</tbody>";

			fclose($myfile);

			echo '<script> document.getElementById("table_div").style.visibility = "visible"; </script>';
		   ?>
		</table>
	</div>


</body>
