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
				$query_array = array();
				//Limit starts at 1000, If the user sets the limit to 0, it will print ALL.
				// $limit_size = 1001;

				echo '<script> document.getElementById("table_div").style.visibility = "hidden"; </script>';

				require '../vendor/autoload.php';

				// $db = new \MongoDB\Driver\Manager('mongodb://localhost:27017');
				$db = new MongoDB\Client('mongodb://localhost:27017');
				$collection = $db->peptide->peptide;

				// $id           = new \MongoDB\BSON\ObjectId('AGQQQPFPPQQPYPQPQPF');
				// $filter      = ['sequence' => $id];
				// $options = [];
                //
				// $query = new \MongoDB\Driver\Query($filter, $options);
				// $rows   = $mongo->executeQuery('peptide.peptide', $query);


				//Preperation of the query array

				//Sequence
				// if (!empty($_GET['seq']))
				// {
				// 	array_push($query_array, array('sequence' => 'AGQQQPFPPQQPYPQPQPF'));//new MongoDB\BSON\Regex ('/' . (string) $_GET['seq'] . '/i'))); // (string) sanitizes the query.
				// }
				// //Min length of Sequence
				// if (!empty($_GET['min']))
				// {
				// 	array_push($query_array, array('sequence' => array('$gt' => (string) $_GET['min'])));
				// }
				// //Max length of Sequence
				// if (!empty($_GET['max']))
				// {
				// 	array_push($query_array, array('sequence' => array('$lt' => (string) $_GET['max'])));
				// }
				// //Limit the number of items to query
				// if (!empty($_GET['count']))
				// {
				// 	//Subtract 1 from limit, to evade a off by one error and print out limit + 1;
				// 	$limit_size = ((int) $_GET['count']) - 1;
				// }
				// //Activities
				// if (isset($_GET['activities'])){
                //
				// 	$activities = $_GET['activities'];
				// 	$not_null = array('$ne' => null);
                //
				// 	foreach($activities as $activity)
				// 	{
				// 		array_push($query_array, array( (string) $activity => $not_null));
				// 	}
				// }

				// if (empty($query_array))
				// {
					$cursor = $collection->find();
				// }
				// else
				// {
					// $cursor = $collection->find($query_array);
				// }

				//Ok, now time to print out the table.

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
				$j = 0;

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
					// //Limit the number of items printed.
					// if ($limit_size != 0)
					// {
					// 	if ($limit_size <= $j)
					// 	{
					// 		break;
					// 	}
					// 	$j++;
					// }
				}
				echo "</tbody>";

				echo '<script> document.getElementById("loading").remove(); </script>';
				echo '<script> document.getElementById("table_div").style.visibility = "visible"; </script>';
		   ?>
		</table>
	</div>


</body>
