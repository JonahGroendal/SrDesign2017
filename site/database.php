<head>
    <?php
		session_start();
		include 'commonLinks.php';
		include 'header.php';
		require 'query.php';

		$array_labels = array("sequence", "type");
		$array_activities = array();
		$myfile = fopen("res/activities.txt", "r") or die("Unable to open file!");
		while(!feof($myfile)) {
			array_push($array_activities, trim(fgets($myfile)));
		}
		fclose($myfile);

		array_pop($array_activities); //removes last item, which is just a '\n'

		$size_activities = count($array_activities);
		$size_labels = count($array_labels);

		$_SESSION['array_activities'] = $array_activities;
		$_SESSION['array_labels'] = $array_labels;
		$_SESSION['size_activities'] = $size_activities;
		$_SESSION['size_labels'] = $size_labels;
	?>
</head>

<body>
	<div class="page">
		<?php
		//Call function to set up query
		$query = setup_query();
		$_SESSION['query'] = $query;
		?>
		<a href="download_query.php" download>Download Query Results as CSV</a>
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
				//Hide document until loading is complete
				echo '<script> document.getElementById("table_div").style.visibility = "hidden"; </script>';

				require 'vendor/autoload.php';


				$db = new MongoDB\Client('mongodb://localhost:27017');
				$collection = $db->peptide->peptide;

				//Limit the number of items to query
				if ($_GET['count'] == "")
				{
					$limit_size = 999;
				}
				else
				{
					$limit_size = ((int) $_GET['count']) - 1;
				}

				//Execute Query
				if (empty($query))
				{
					$cursor = $collection->find();
				}
				else
				{
					$cursor = $collection->find($query);
				}

				//Ok, now time to print out the table.
				echo "<thead><tr>";

				//Print labels
				for ($i = 0; $i < $size_labels; $i++)
				{
					echo '<th>' . $array_labels[$i] . '</th>';
				}
				for ($i = 0; $i < $size_activities; $i++)
				{
					if ($size_activities > 5)
					{
						echo '<th id = "' .
						$array_activities[$i] .
						'" onmouseover="this.innerHTML=\'' .
						$array_activities[$i] .
						'\';" onmouseout="this.innerHTML=\'*\';" onclick="click_on(\'' .
						$array_activities[$i] .
						'\')">*</th>';
					}
				}

				echo "</tr></thead><tbody>";
				$j = 0;

				//Print table body
				foreach ($cursor as $doc)
				{
					$array = iterator_to_array($doc);
					//Sequence
					if(isset($array["sequence"]) && strlen($array["sequence"]) <= 50) //Check if empty
					{
						echo "<tr><td>" . $array["sequence"] . "</td>";

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
					else
					{
						$j--;
					}
					//Limit the number of items printed.
					if ($limit_size != -1)
					{
						if ($limit_size <= $j)
						{
							break;
						}
						$j++;
					}
				}
				echo "</tbody>";

				//Remove Loading text
				echo '<script> document.getElementById("loading").remove(); </script>';
				//Unhide Table.
				echo '<script> document.getElementById("table_div").style.visibility = "visible"; </script>';
		   ?>
		</table>
	</div>


</body>
