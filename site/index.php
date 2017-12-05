<head>
    <?php
		include 'php/commonLinks.php';
		include 'php/header.php';
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
        <h3>Query Database</h3>
        <h5>Leave field alone if you don't want to query by that
            <table class="table">
                <thead>
                    <tr>
                        <th>
                            Sequence
                        </th>
                        <th>
                            Activity
                        </th>
                        <th>
                            Submit
                        </th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <th>
                            <input type="text" name="seq" form="query_form" style="width:100%;max-width:90%;">
                        </th>
                        <th>
                            <select form="query_form" name="activity" style="width:100%;max-width:90%;">
                                <option value="None">All</option>
                                <?php
                                    $array_labels = array("sequence", "name", "type");
                                    $array_activities = array();
                                    $myfile = fopen("res/activities.txt", "r") or die("Unable to open file!");
                                    while(!feof($myfile)) {
                                      array_push($array_activities, trim(fgets($myfile)));
                                    }
                                    fclose($myfile);

                                    array_pop($array_activities); //removes last item, which is just a '\n'

                                    $size_activities = count($array_activities);
                                    $size_labels = count($array_labels);
                                    for ($i = 0; $i < $size_activities; $i++)
                                    {
                                        echo '<option value="' . $array_activities[$i] . '">' . $array_activities[$i] . '</option>';
                                    }
                                ?>
                            </select>
                        </th>
                        <th>
                            <form action="php/database.php" method="post" id="query_form"><input type="submit">
                            </form>
                        </th>
                    </tr>
                </tbody>
            </table>
    </div>
    <div class="page" style="margin-top:10px">
        <h3>
			<script type="text/javascript">
				function AlertIt() {
					var answer = confirm ("Loading Full database might take some time.")
					if (answer)
						window.location="php/database.php";
				}
			</script>

			<a href="javascript:AlertIt();">Go to Full Database</a>
		</h3>
    </div>
    <div class="page" style="margin-top:100px">
        <h3>Authors</h3>
        <h5>Jacob Schuurmans</h5>
        <h5>Jack McClure</h5>
        <h5>Jonah Groendal</h5>
        <h5>Angelo Danducci</h5>
        <h5>Josh Looney</h5>
</body>
