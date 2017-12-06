<head>
    <?php
		include 'php/commonLinks.php';
		include 'php/header.php';

		$array_labels = array("sequence", "name", "type");
		$array_activities = array();
		$myfile = fopen("res/activities.txt", "r") or die("Unable to open file!");
		while(!feof($myfile)) {
			array_push($array_activities, trim(fgets($myfile)));
			error_log($array_activities[0]);
		}
		fclose($myfile);

		array_pop($array_activities); //removes last item, which is just a '\n'
		$size_activities = count($array_activities);
		$size_labels = count($array_labels);
	?>
</head>
    <div class="page">
      <h1>Peptide Database</h1>
    </div>
    <div class="page" style="margin-top:10px">
        <h3>About</h3>
        <h4>
            This website has a collection of many different peptide databases used for machine learning purposes.
        </h4>
    </div>
	<div class="page" style="margin-top:10px">
		<h3>Query Form</h3>
		<div class="tablepage">
			<table class="table">
                <thead>
                    <tr>
                        <th>
                            Sequence (Partial or full)
                        </th>
                        <th>
                            Length (low, Min of 1))
                        </th>
						<th>
                        </th>
						<th>
                            Length (high, Max of 50)
                        </th>
						<th>
							Count (Leave blank for all)
						</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>
                            <input type="text" name="seq" form="query_form" style="width:100%;max-width:90%;">
                        </td>
                        <td>
                            <input type="text" name="min" form="query_form">
                        </td>
						<td>to</td>
						<td>
							<input type="text" name="max" form="query_form">
						</td>
						<td>
							<input type="text" name="count" form="query_form">
						</td>
                    </tr>
                </tbody>
			</table>
		</div>
		<div class="tablepage"> <!-- ADD THIS STYLE IF THE LIST IS GETTING LONG :  style="overflow-y:scroll; height:250px" -->
			<table class="table">
				<thead>
					<th>
						Activities
					</th>
					<th>
					</th>
				</thead>
				<tbody>
					<?php
					for ($i = 0; $i < $size_activities; $i++)
					{
						echo '<tr><td>' . $array_activities[$i] . '</td><td><input type="checkbox" name="activities[] id="activities" form="query_form" value="' . $array_activities[$i] . '"></td></tr>';
					}
					?>
				</tbody>
			</table>
		</div>
			<form action="php/database.php" method="get" id="query_form"><input type="submit" style="width:100%">
			</form>
	</div>
    <div class="page" style="margin-top:100px">
        <h3>Authors</h3>
        <h5>Jacob Schuurmans</h5>
        <h5>Jack McClure</h5>
        <h5>Jonah Groendal</h5>
        <h5>Angelo Danducci</h5>
        <h5>Josh Looney</h5>
	</div>
</body>

<!-- <script type="text/javascript">
	function AlertIt() {
		var answer = confirm ("Loading Full database might take some time.")
		if (answer)
			window.location="php/database.php";
	}
</script> -->
