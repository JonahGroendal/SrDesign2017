<?php session_start(); include 'conn.php';?>
<head>
    <?php include 'commonLinks.php'; ?>
    <link rel="stylesheet" type="text/css" href="login-register-style.css">
</head>
<body  background="res/Homepagebackground.jpg" style="background-position: top center;">
    <?php include 'header.php'; ?>
    <div class="page">
        <?php
        if (!isset($_SESSION['id'])) {
        ?>
      <div class="page-header">
         <h2>Login</h2>
      </div>
      <form role="form" class="form-horizontal" method="POST" action="account.php">
          <input type="hidden" name="login" value="1">
           <div class="form-group">
             <label for="first" class="col-md-3 control-label">Email</label>
             <div class="col-md-9">
             <input type="email" class="field-style" name="email">
             </div>
           </div>
           <div class="form-group">
             <label for="last" class="col-md-3 control-label">Password</label>
             <div class="col-md-9">
             <input type="password" class="field-style" name="password">
             </div>
		 </div>
        <div class="form-group">
          <div class="col-md-offset-3 col-md-9">
            <button type="submit" class="btn btn-primary" style="font-weight:bold;">Login</button>
          </div>
        </div>
        </form>
        <?php
        if (isset($_GET['failed'])) {
            echo '<div id="imgUploadError" class="alert alert-danger" role="alert">Login Failed</div>';
        }

            } else {
        ?>
        <h3><a href="logout.php">Logout?</a></h3>
        <?php
            }
        ?>
    </div>
</body>
