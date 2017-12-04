<?php
$array_labels = array("sequence", "name", "type");
$array_activities = array();
$myfile = fopen("../res/activities.txt", "r") or die("Unable to open file!");
while(!feof($myfile)) {
  array_push($array_activities, trim(fgets($myfile)));
}
fclose($myfile);
array_pop($array_activities); //removes last item, which is just a '\n'
$size = count($array_activities);
$size_labels = count($array_labels);
 ?>
