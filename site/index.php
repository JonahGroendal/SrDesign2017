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
</body>
