<head>
    <?php
		include 'commonLinks.php';
		include 'header.php';
	?>
</head>

<div id="table" class="tablepage dataTables_wrapper form-inline dt-bootstrap no-footer">
   <!-- <div class="row">
      <div class="col-sm-6">
         <div class="dataTables_length" id="example_length">
            <label>
               Show
               <select name="example_length" aria-controls="example" class="form-control input-sm">
                  <option value="10">10</option>
                  <option value="25">25</option>
                  <option value="50">50</option>
                  <option value="100">100</option>
               </select>
               entries
            </label>
         </div>
      </div>
      <div class="col-sm-6">
         <div id="example_filter" class="dataTables_filter">
            <label>Search:<input type="search" class="form-control input-sm" placeholder="" aria-controls="example">
            </label>
         </div>
      </div>
   </div> -->
   <div class="row">
      <div class="col-sm-12">
         <table id="example" class="table table-striped table-bordered dataTable no-footer" cellspacing="0" width="100%" role="grid" aria-describedby="example_info" style="width: 100%;">
            <thead>
               <tr role="row">
                  <th class="sorting_asc" tabindex="0" aria-controls="example" rowspan="1" colspan="1" aria-sort="ascending" aria-label="Name: activate to sort column descending" style="width: 142px;">Name</th>
                  <th class="sorting" tabindex="0" aria-controls="example" rowspan="1" colspan="1" aria-label="Position: activate to sort column ascending" style="width: 237px;">Position</th>
                  <th class="sorting" tabindex="0" aria-controls="example" rowspan="1" colspan="1" aria-label="Office: activate to sort column ascending" style="width: 104px;">Office</th>
                  <th class="sorting" tabindex="0" aria-controls="example" rowspan="1" colspan="1" aria-label="Salary: activate to sort column ascending" style="width: 80px;">Salary</th>
               </tr>
            </thead>
            <tbody>
               <tr role="row" class="odd">
                  <td class="sorting_1">Tiger Nixon</td>
                  <td>System Architect</td>
                  <td>Edinburgh</td>
                  <td>$320,800</td>
               </tr>
               <tr role="row" class="even">
                  <td class="sorting_1">Timothy Mooney</td>
                  <td>Office Manager</td>
                  <td>London</td>
                  <td>$136,200</td>
               </tr>
               <tr role="row" class="odd">
                  <td class="sorting_1">Unity Butler</td>
                  <td>Marketing Designer</td>
                  <td>San Francisco</td>
                  <td>$85,675</td>
               </tr>
               <tr role="row" class="even">
                  <td class="sorting_1">Vivian Harrell</td>
                  <td>Financial Controller</td>
                  <td>San Francisco</td>
                  <td>$452,500</td>
               </tr>
               <tr role="row" class="odd">
                  <td class="sorting_1">Yuri Berry</td>
                  <td>Chief Marketing Officer (CMO)</td>
                  <td>New York</td>
                  <td>$675,000</td>
               </tr>
               <tr role="row" class="even">
                  <td class="sorting_1">Zenaida Frank</td>
                  <td>Software Engineer</td>
                  <td>New York</td>
                  <td>$125,250</td>
               </tr>
               <tr role="row" class="odd">
                  <td class="sorting_1">Zorita Serrano</td>
                  <td>Software Engineer</td>
                  <td>San Francisco</td>
                  <td>$115,000</td>
               </tr>
            </tbody>
         </table>
      </div>
   </div>
   <div class="row">
      <div class="col-sm-5">
         <div class="dataTables_info" id="example_info" role="status" aria-live="polite">Showing 51 to 57 of 57 entries</div>
      </div>
      <div class="col-sm-7">
         <div class="dataTables_paginate paging_simple_numbers" id="example_paginate">
            <ul class="pagination">
               <li class="paginate_button previous" id="example_previous">
                  <a href="https://www.datatables.net/manual/styling/bootstrap-simple.html#" aria-controls="example" data-dt-idx="0" tabindex="0">Previous</a>
               </li>
               <li class="paginate_button ">
                  <a href="https://www.datatables.net/manual/styling/bootstrap-simple.html#" aria-controls="example" data-dt-idx="1" tabindex="0">1</a>
               </li>
               <li class="paginate_button ">
                  <a href="https://www.datatables.net/manual/styling/bootstrap-simple.html#" aria-controls="example" data-dt-idx="2" tabindex="0">2</a>
               </li>
               <li class="paginate_button ">
                  <a href="https://www.datatables.net/manual/styling/bootstrap-simple.html#" aria-controls="example" data-dt-idx="3" tabindex="0">3</a>
               </li>
               <li class="paginate_button ">
                  <a href="https://www.datatables.net/manual/styling/bootstrap-simple.html#" aria-controls="example" data-dt-idx="4" tabindex="0">4</a>
               </li>
               <li class="paginate_button ">
                  <a href="https://www.datatables.net/manual/styling/bootstrap-simple.html#" aria-controls="example" data-dt-idx="5" tabindex="0">5</a>
               </li>
               <li class="paginate_button active">
                  <a href="https://www.datatables.net/manual/styling/bootstrap-simple.html#" aria-controls="example" data-dt-idx="6" tabindex="0">6</a>
               </li>
               <li class="paginate_button next disabled" id="example_next">
                  <a href="https://www.datatables.net/manual/styling/bootstrap-simple.html#" aria-controls="example" data-dt-idx="7" tabindex="0">Next</a>
               </li>
            </ul>
         </div>
      </div>
   </div>
</div>
</div>    <!-- <div class="tabepage container" style="margin-top:10px">
		<table id="table" class="display" cellspacing="0" width="100%"><thead><tr><th>Name</th><th>Position</th><th>Office</th><th>Salary</th></tr></thead><tbody><tr><td>Tiger Nixon</td><td>System Architect</td><td>Edinburgh</td><td>$320,800</td></tr><tr><td>Garrett Winters</td><td>Accountant</td><td>Tokyo</td><td>$170,750</td></tr><tr><td>Ashton Cox</td><td>Junior Technical Author</td><td>San Francisco</td><td>$86,000</td></tr><tr><td>Cedric Kelly</td><td>Senior Javascript Developer</td><td>Edinburgh</td><td>$433,060</td></tr><tr><td>Airi Satou</td><td>Accountant</td><td>Tokyo</td><td>$162,700</td></tr><tr><td>Brielle Williamson</td><td>Integration Specialist</td><td>New York</td><td>$372,000</td></tr><tr><td>Herrod Chandler</td><td>Sales Assistant</td><td>San Francisco</td><td>$137,500</td></tr><tr><td>Rhona Davidson</td><td>Integration Specialist</td><td>Tokyo</td><td>$327,900</td></tr><tr><td>Colleen Hurst</td><td>Javascript Developer</td><td>San Francisco</td><td>$205,500</td></tr><tr><td>Sonya Frost</td><td>Software Engineer</td><td>Edinburgh</td><td>$103,600</td></tr><tr><td>Jena Gaines</td><td>Office Manager</td><td>London</td><td>$90,560</td></tr><tr><td>Quinn Flynn</td><td>Support Lead</td><td>Edinburgh</td><td>$342,000</td></tr><tr><td>Charde Marshall</td><td>Regional Director</td><td>San Francisco</td><td>$470,600</td></tr><tr><td>Haley Kennedy</td><td>Senior Marketing Designer</td><td>London</td><td>$313,500</td></tr><tr><td>Tatyana Fitzpatrick</td><td>Regional Director</td><td>London</td><td>$385,750</td></tr><tr><td>Michael Silva</td><td>Marketing Designer</td><td>London</td><td>$198,500</td></tr><tr><td>Paul Byrd</td><td>Chief Financial Officer (CFO)</td><td>New York</td><td>$725,000</td></tr><tr><td>Gloria Little</td><td>Systems Administrator</td><td>New York</td><td>$237,500</td></tr><tr><td>Bradley Greer</td><td>Software Engineer</td><td>London</td><td>$132,000</td></tr><tr><td>Dai Rios</td><td>Personnel Lead</td><td>Edinburgh</td><td>$217,500</td></tr><tr><td>Jenette Caldwell</td><td>Development Lead</td><td>New York</td><td>$345,000</td></tr><tr><td>Yuri Berry</td><td>Chief Marketing Officer (CMO)</td><td>New York</td><td>$675,000</td></tr><tr><td>Caesar Vance</td><td>Pre-Sales Support</td><td>New York</td><td>$106,450</td></tr><tr><td>Doris Wilder</td><td>Sales Assistant</td><td>Sidney</td><td>$85,600</td></tr><tr><td>Angelica Ramos</td><td>Chief Executive Officer (CEO)</td><td>London</td><td>$1,200,000</td></tr><tr><td>Gavin Joyce</td><td>Developer</td><td>Edinburgh</td><td>$92,575</td></tr><tr><td>Jennifer Chang</td><td>Regional Director</td><td>Singapore</td><td>$357,650</td></tr><tr><td>Brenden Wagner</td><td>Software Engineer</td><td>San Francisco</td><td>$206,850</td></tr><tr><td>Fiona Green</td><td>Chief Operating Officer (COO)</td><td>San Francisco</td><td>$850,000</td></tr><tr><td>Shou Itou</td><td>Regional Marketing</td><td>Tokyo</td><td>$163,000</td></tr><tr><td>Michelle House</td><td>Integration Specialist</td><td>Sidney</td><td>$95,400</td></tr><tr><td>Suki Burks</td><td>Developer</td><td>London</td><td>$114,500</td></tr><tr><td>Prescott Bartlett</td><td>Technical Author</td><td>London</td><td>$145,000</td></tr><tr><td>Gavin Cortez</td><td>Team Leader</td><td>San Francisco</td><td>$235,500</td></tr><tr><td>Martena Mccray</td><td>Post-Sales support</td><td>Edinburgh</td><td>$324,050</td></tr><tr><td>Unity Butler</td><td>Marketing Designer</td><td>San Francisco</td><td>$85,675</td></tr><tr><td>Howard Hatfield</td><td>Office Manager</td><td>San Francisco</td><td>$164,500</td></tr><tr><td>Hope Fuentes</td><td>Secretary</td><td>San Francisco</td><td>$109,850</td></tr><tr><td>Vivian Harrell</td><td>Financial Controller</td><td>San Francisco</td><td>$452,500</td></tr><tr><td>Timothy Mooney</td><td>Office Manager</td><td>London</td><td>$136,200</td></tr><tr><td>Jackson Bradshaw</td><td>Director</td><td>New York</td><td>$645,750</td></tr><tr><td>Olivia Liang</td><td>Support Engineer</td><td>Singapore</td><td>$234,500</td></tr><tr><td>Bruno Nash</td><td>Software Engineer</td><td>London</td><td>$163,500</td></tr><tr><td>Sakura Yamamoto</td><td>Support Engineer</td><td>Tokyo</td><td>$139,575</td></tr><tr><td>Thor Walton</td><td>Developer</td><td>New York</td><td>$98,540</td></tr><tr><td>Finn Camacho</td><td>Support Engineer</td><td>San Francisco</td><td>$87,500</td></tr><tr><td>Serge Baldwin</td><td>Data Coordinator</td><td>Singapore</td><td>$138,575</td></tr><tr><td>Zenaida Frank</td><td>Software Engineer</td><td>New York</td><td>$125,250</td></tr><tr><td>Zorita Serrano</td><td>Software Engineer</td><td>San Francisco</td><td>$115,000</td></tr><tr><td>Jennifer Acosta</td><td>Junior Javascript Developer</td><td>Edinburgh</td><td>$75,650</td></tr><tr><td>Cara Stevens</td><td>Sales Assistant</td><td>New York</td><td>$145,600</td></tr><tr><td>Hermione Butler</td><td>Regional Director</td><td>London</td><td>$356,250</td></tr><tr><td>Lael Greer</td><td>Systems Administrator</td><td>London</td><td>$103,500</td></tr><tr><td>Jonas Alexander</td><td>Developer</td><td>San Francisco</td><td>$86,500</td></tr><tr><td>Shad Decker</td><td>Regional Director</td><td>Edinburgh</td><td>$183,000</td></tr><tr><td>Michael Bruce</td><td>Javascript Developer</td><td>Singapore</td><td>$183,000</td></tr><tr><td>Donna Snider</td><td>Customer Support</td><td>New York</td><td>$112,000</td></tr></tbody></table>
    </div> -->

	<script type="text/javascript">
		// For demo to fit into DataTables site builder...
		$('#example')
			.removeClass( 'display' )
			.addClass('table table-striped table-bordered');
	</script>
</body>
