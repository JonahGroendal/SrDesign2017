function hover_on(id)
{
	document.getElementById(id).innerHTML = id;

}

function hover_off(id, text)
{
	document.getElementById(id).innerHTML = '*';
}

function click_on(id)
{
	document.getElementById(id).onclick = function() {do_nothing()}; //Refer to function click_off()
	document.getElementById(id).onmouseover = function() {do_nothing()};
	document.getElementById(id).onmouseout = function() {do_nothing()};
}

//Currently Unused
function click_off(id) //Switch onclick to this function in function click_on(). This will enable switching between perminent labels. Though it also sorts them. So IDK.
{
	document.getElementById(id).onmouseover = function() {hover_on(id)};
	document.getElementById(id).onmouseout = function() {hover_off(id)};
	document.getElementById(id).onclick = function() {click_on(id)};
}

function do_nothing(){}
