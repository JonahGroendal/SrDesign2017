<?php
function setup_query()
{
	//Preperation of the query array
	$query = array();
	//Sequence
	if (!empty($_GET['seq']))
	{
		// array_push($query, array('sequence' => array($regex => "/^" . ( (string) $_GET['seq'] ) . "/i")));
		$regex = new MongoDB\BSON\Regex (".*" . ((string) $_GET['seq']) . ".*");
		array_push($query, array('sequence' => $regex));
	}
	//Min length of Sequence
	if (!empty($_GET['min']))
	{
		if (!empty($_GET['max']))
		{
			$min = array('$where' => "(this.sequence.length > ". ((string)$_GET['min']) .")");
			$max = array('$where' => "(this.sequence.length < ". ((string)$_GET['max']) .")");
			$length_query = array('$and' => array($min, $max));
			array_push($query, $length_query);
		}
		else
		{
			array_push($query, array('$where' => "(this.sequence.length > ". ((string)$_GET['min']) .")"));
		}
	}
	else
	{
		if (!empty($_GET['max']))
		{
			array_push($query, array('$where' => "(this.sequence.length < ". ((string)$_GET['max']) .")"));
		}
	}

	//Activities True
	if (isset($_GET['activities_true'])){

		$activities = $_GET['activities_true'];

		foreach($activities as $activity)
		{
			//Use array('$ne' => null) and not 'true', True breaks floating point values, since some activities are not simply 1 or 0
			array_push($query, array( (((string)$activity) . '.value') => array('$ne' => null)));
		}
	}

	//Activities False
	if (isset($_GET['activities_false'])){

		$activities = $_GET['activities_false'];

		foreach($activities as $activity)
		{
			array_push($query, array( (((string)$activity) . '.value') => false));
		}
	}

	//Set up Logic
	if(!empty($query))
	{
		if (isset($_GET['logic']))
		{
			$query = array(('$' . ((string)$_GET['logic'])) => $query);
		}
		else
		{
			$query = array('$AND' => $query);
		}
	}

	return $query;
}
?>
