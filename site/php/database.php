<head>
    <?php
		include 'commonLinks.php';
		include 'header.php';

		$array_labels = array("sequence", "name", "type");
		$array_activities = array();
		$myfile = fopen("../res/activities.txt", "r") or die("Unable to open file!");
		while(!feof($myfile)) {
			array_push($array_activities, trim(fgets($myfile)));
		}
		fclose($myfile);

		array_pop($array_activities); //removes last item, which is just a '\n'

		$size_activities = count($array_activities);
		$size_labels = count($array_labels);
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
	<div id="table_div" class="page form-inline no-footer">
		<table id="peptide_table" class="table table-bordered">
			<?php
				// echo "<div>";
				// if (!empty($_GET['seq']))
				// {
				// 	echo "<h3>SEQ:" . $_GET['seq'] . "</h3>";
				// }
				// if (!empty($_GET['min']))
				// {
				// 	echo "<h3>MIN:" . $_GET['min'] . "</h3>";
				// }
				// if (!empty($_GET['max']))
				// {
				// 	echo "<h3>MAX:" . $_GET['max'] . "</h3>";
				// }
				// if (!empty($_GET['count']))
				// {
				// 	echo "<h3>COUNT:" . $_GET['count'] . "</h3>";
				// }
				// if (isset($_GET['activities'])){
				// 	$activities = $_GET['activities'];
				// 	foreach($activities as $activity)
				// 	{
				// 		echo '<h2>' . $activity . '</h2>';
				// 	}
				// }
			?>
			<?php
		  		echo '<script> document.getElementById("table_div").style.visibility = "hidden"; </script>';

				$not_null = array('$ne' => null);

				require '../vendor/autoload.php';

				$db = new MongoDB\Client("mongodb://localhost:27017");

				$collection = $db->peptide->peptide;
				// $cursor = $collection->find(array("antibacterial" => $not_null)); //WORKS
				$cursor = $collection->find();

				echo "<thead><tr>";

				//Print labels
				for ($i = 0; $i < $size_labels; $i++)
				{
					echo '<th>' . $array_labels[$i] . '</th>';
				}
				for ($i = 0; $i < $size_activities; $i++)
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
						for($i = 0; $i < $size_activities; $i++)
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
