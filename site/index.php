<head>
    <?php
		include 'commonLinks.php';
		include 'header.php';

		$array_labels = array("sequence", "name", "type");
		$array_activities = array();
		$myfile = fopen("res/activities.txt", "r") or die("Unable to open file!");
		while(!feof($myfile)) {
			array_push($array_activities, trim(fgets($myfile)));
		}
		fclose($myfile);

		array_pop($array_activities); //removes last item, which is just a newline
		$size_activities = count($array_activities);
		$size_labels = count($array_labels);
	?>
</head>
<body>
    <div class="page">
      <h1>Peptide Database</h1>
    </div>
    <div class="page" style="margin-top:10px">
		<h4>WMU Peptide is a free access database of experimentally verified peptides that have been compiled together from various public sources.<br><br>
		It combines data from separate databases with different focuses to give a straightforward representation of biological activity observed for each peptide as well as a link to each source of an activity.</h4>
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
							Count (Blank for 1k Entries. 0 for ALL)
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
		<div class="tablepage">
			<table class="table">
				<thead>
					<th>
						Logical Operators
					</th>
					<th>
						Default is "AND"
					</th>
				</thead>
				<tbody>
					<tr>
						<td>
							OR
						</td>
						<td>
							<input type="radio" name="logic" id="activities" form="query_form" value="or">
						</td>
						<td>
					</tr>
					<tr>
						<td>
							NOR
						</td>
						<td>
							<input type="radio" name="logic" id="activities" form="query_form" value="nor">
						</td>
					</tr>
					<tr>
						<td>
							AND
						</td>
						<td>
							<input type="radio" name="logic" id="activities" form="query_form" checked="checked" value="and">
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
						isTrue
					</th>
					<th>
						isFalse
					</th>
					<th>
						Activities
					</th>
					<th>
						isTrue
					</th>
					<th>
						isFalse
					</th>
				</thead>
				<tbody>
					<?php
					for ($i = 0; $i < $size_activities; $i++)
					{
						if($i%2==0)
							echo '<tr><td>' . $array_activities[$i] . '</td><td><input type="checkbox" name="activities_true[] id="activities" form="query_form" value="' . $array_activities[$i] . '"></td></td><td><input type="checkbox" name="activities_false[] id="activities" form="query_form" value="' . $array_activities[$i] . '"></td>';
						else
							echo '<td>' . $array_activities[$i] . '</td><td><input type="checkbox" name="activities_true[] id="activities" form="query_form" value="' . $array_activities[$i] . '"></td></td><td><input type="checkbox" name="activities_false[] id="activities" form="query_form" value="' . $array_activities[$i] . '"></td></tr>';
					}
					?>
				</tbody>
			</table>
		</div>
			<form action="database.php" method="get" id="query_form"><input type="submit" style="width:100%">
			</form>
	</div>
</body>
