function test (){
	$.ajax({
	    type: 'POST',
	    url: 'mongotest.php',
	    success: function(data)
		{
			console.log(data);
	    }
	});
}
