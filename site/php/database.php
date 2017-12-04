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
		  	echo '<script> document.getElementById("peptide_table").style.visibility = "hidden"; </script>';
			$array_labels = array("sequence", "name", "type");
			$array_activites = array("hydrophobicity","toxic", "immunogenic", "insecticidal", "allergen", "antibacterial", "anticancer", "antifungal", "antihyptertensive", "antimicrobial", "antiparasitic", "antiviral");
			$size = count($array_activites);
			$size_labels = count($array_labels);
			echo "<thead><tr>";

			for ($i = 0; $i < $size_labels; $i++)
			{
				echo '<th>' . $array_labels[$i] . '</th>';
			}
			for ($i = 0; $i < $size; $i++)
			{
				echo '<th id = "' .
				$array_activites[$i] .
				'" onmouseover="this.innerHTML=\'' .
				$array_activites[$i] .
				'\';" onmouseout="this.innerHTML=\'*\';" onclick="click_on(\'' .
				$array_activites[$i] .
				'\')">*</th>';
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
				if(isset($array["sequence"]))
				{
					echo "<tr><td>" . $array["sequence"] . "</td>";
					//Name
					echo "<td>NA</td>";
					//Type
					if(isset($array["type"]))
					{
						if (isset(iterator_to_array($array["type"])["value"]))
						{
							echo "<td>" . iterator_to_array($array["type"])["value"] . "</td>";
						}
						else
						{
							echo "<td>NA</td>";
						}
					}
					else
					{
						echo "<td>NA</td>";
					}
					//Activities
					for($i = 0; $i < $size; $i++)
					{
						if (isset($array[$array_activites[$i]]) && !strcmp(iterator_to_array($array[$array_activites[$i]])["value"], " "))
						{
							echo "<td>" . iterator_to_array($array[$array_activites[$i]])["value"] . "</td>";
						}
						else
						{
							// if ($array["sequence"] === "YVRGMASKAGAIAGKIAKVALKAL")
							// {
							// 	// error_log("DEBUG :" . isset($array["toxic"]) . ":");
							// 	if(isset($array["toxic"]))
							// 	{
							// 		error_log("TEST");
							// 	}
							// 	else
							// 	{
							// 		error_log("FUCK YOU");
							// 	}
							// }
							echo "<td>NA</td>";
						}
					}
					echo "</tr>";
				}
			}
			echo "</tbody>";

			echo '<script> document.getElementById("peptide_table").style.visibility = "visible"; </script>';
		   ?>
		</table>
	</div>


</body>
