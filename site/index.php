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
                            Institution
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
                            <input type="text" name="seq" form="query_form">
                        </th>
                        <th>
                            <select form="query_form" name="institution" style="width:100%;max-width:90%;">
                                <option value="None">None</option>
                                <option value="WMU">WMU</option>
                                <option value="CMU">CMU</option>
                            </select>
                        </th>
                        <th>
                            <select form="query_form" name="activity" style="width:100%;max-width:90%;">
                                <option value="None">None</option>
                                <option value="hydrophobicity" >Hydrophobicity</option>
                                <option value="allergen">Allergen</option>
                            </select>
                        </th>
                        <th>
                            <form action="php/test.php" method="post" id="query_form"><input type="submit">
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
        <h5>Jack</h5>
        <h5>Jonah</h5>
        <h5>Angelo</h5>
        <h5>Josh</h5>
</body>
