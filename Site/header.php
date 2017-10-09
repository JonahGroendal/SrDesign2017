<?php session_start();?>
<nav class="navbar navbar-default navbar-fixedtop affix-top nav-style">
    <div class="navbar-inner">
       <div class="container-fluid">
           <div class="navbar-header">
               <a class="navbar-brand page-scroll" href="index.php">Peptide Database</a>
           </div>
		   <ul class="nav navbar-nav navbar-right">
			   <?php
			   if (!isset($_SESSION['id'])) {
			   ?>
			   <li>
				   <a class="page-scroll" href="login.php">Login</a>
				   <a class="page-scroll" onclick="test()">TEST</a>
			   </li>
			   <?php
			   } else {
			   ?>
			   <li>
				   <a class="page-scroll" href="logout.php">Logout</a>
			   </li>
			   <?php
			   }
			   ?>
		   </ul>
       </div>
   </div>
</nav>
