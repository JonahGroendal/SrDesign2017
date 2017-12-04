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
	<div id="loading" class ="page"><h3>Loading . . .</h3></div>
	<div id="table_div" class="tablepage form-inline no-footer">
		<table id="peptide_table" class="table table-bordered">
		  <?php
		  	echo '<script> document.getElementById("table_div").style.visibility = "hidden"; </script>';

			$not_null = array('$ne' => null);

			require '../vendor/autoload.php';
			require 'get_metadata.php';

			$db = new MongoDB\Client("mongodb://localhost:27017");


			$collection = $db->peptide->peptide;
			$cursor = $collection->find(array("antibacterial" => $not_null)); //WORKS

			echo "<thead><tr>";

			//Print labels
			for ($i = 0; $i < $size_labels; $i++)
			{
				echo '<th>' . $array_labels[$i] . '</th>';
			}
			for ($i = 0; $i < $size; $i++)
			{
				echo '<th id = "' .
				$array_activities[$i] .
				'" onmouseover="this.innerHTML=\'' .
				$array_activities[$i] .
				'\';" onmouseout="this.innerHTML=\'*\';" onclick="click_on(\'' .
				$array_activities[$i] .
				'\')">*</th>';
			}

			echo "</tr></thead><tbody>";

			foreach ($cursor as $doc)
			{
				$array = iterator_to_array($doc);
				//Sequence
				if(isset($array["sequence"]) && strlen($array["sequence"]) <= 50) //Check if empty
				{
					echo "<tr><td>" . $array["sequence"] . "</td>";
					//Name
					echo "<td>NA</td>";
					//Type
					if(isset($array["type"])) //Check if empty
					{
						echo "<td>" . iterator_to_array($array["type"])["value"] . "</td>";
					}
					else
					{
						echo "<td>NA</td>";
					}
					//Activities
					for($i = 0; $i < $size; $i++)
					{
						if (isset($array[$array_activities[$i]])) //Check if empty
						{
							if (iterator_to_array($array[$array_activities[$i]])["value"] == false)
							{
								echo "<td>" . 0 . "</td>";
							}
							else //Is true or has value
							{
							echo "<td>" . iterator_to_array($array[$array_activities[$i]])["value"] . "</td>";
							}
						}
						else
						{
							echo "<td>NA</td>";
						}
					}
					echo "</tr>";
				}
			}
			echo "</tbody>";

			echo '<script> document.getElementById("loading").remove(); </script>';
			echo '<script> document.getElementById("table_div").style.visibility = "visible"; </script>';
		   ?>
		</table>
	</div>


</body>
