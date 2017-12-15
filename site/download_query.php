<?php
	//Lets the broswer know this is a file to download, not a webpage
	header ("Content-Type: application/octet-stream");
	header ("Content-disposition: attachment; filename=download.csv");

	//Setup variables
	session_start();
	$query = $_SESSION['query'];

	$array_activities = $_SESSION['array_activities'];
	$array_labels = $_SESSION['array_labels'];
	$size_activities = $_SESSION['size_activities'];
	$size_labels = $_SESSION['size_labels'];

	require 'vendor/autoload.php';

	$db = new MongoDB\Client('mongodb://localhost:27017');
	$collection = $db->peptide->peptide;

	//Execute Query
	if (empty($query))
	{
		$cursor = $collection->find();
	}
	else
	{
		$cursor = $collection->find($query);
	}

	//Print labels
	for ($i = 0; $i < $size_labels; $i++)
	{
		echo $array_labels[$i] . ",";
	}
	for ($i = 0; $i < $size_activities; $i++)
	{
		if ($size_activities > 5)
		{
			echo $array_activities[$i] . ",";
		}
	}

	echo "\n";

	foreach ($cursor as $doc)
	{
		$array = iterator_to_array($doc);
		//Sequence
		if(isset($array["sequence"]) && strlen($array["sequence"]) <= 50) //Check if empty
		{
			echo $array["sequence"] . ",";
			//Type
			if(isset($array["type"])) //Check if empty
			{
				echo iterator_to_array($array["type"])["value"] . ",";
			}
			else
			{
				echo "None,";
			}
			//Activities
			for($i = 0; $i < $size_activities; $i++)
			{
				if (isset($array[$array_activities[$i]])) //Check if empty
				{
					if (iterator_to_array($array[$array_activities[$i]])["value"] == false)
					{
						echo 0 . ",";
					}
					else //Is true or has value
					{
					echo iterator_to_array($array[$array_activities[$i]])["value"] . ",";
					}
				}
				else
				{
					echo "None,";
				}
			}
			echo "\n";
		}
	}
?>
