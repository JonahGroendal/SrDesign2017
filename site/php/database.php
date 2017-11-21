<head>
    <?php
		include 'commonLinks.php';
		include 'header.php';
	?>
</head>

<body>
	<div class="tablepage form-inline no-footer">
		<table id="table" class="table table-bordered">
		  <?php
				$myfile = fopen("../res/db_dump.csv", "r") or die("Unable to open file!");

				$line = fgets($myfile);
				$tokens = explode("|", $line);

				echo "<thead><tr>";

				for ($i = 0; $i < count($tokens); $i++)
				{
					echo "<th>" . trim($tokens[$i]) . "</th>";
				}

				echo "</tr></thead><tbody>";

				while (!feof($myfile))
				{
					$line = fgets($myfile);
					$tokens = explode("|", $line);


					if (strlen(trim($tokens[0])) < 50)
					{
						echo "<tr>";
						for ($i = 0; $i < count($tokens); $i++)
						{
							echo "<td>" . trim($tokens[$i]) . "</td>";
						}
						echo "</tr>";
					}
				}

				echo "</tbody>";

				fclose($myfile);
		   ?>
		</table>
	</div>

	<script type="text/javascript" charset="utf-8">
		$(document).ready(function() {
			$('#table').DataTable();
		} );
	</script>

</body>
