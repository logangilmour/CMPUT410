<html> 
<head> 
<script type="text/javascript"> 
function ajax(){ 
	xmlhttp=new XMLHttpRequest(); 
	xmlhttp.onreadystatechange=function(){ 
		document.getElementById("meter-box").innerHTML=xmlhttp.responseText; 
	}
	var val = document.getElementById("feet-box").value;	
	xmlhttp.open("GET","lab9.php?q="+val,true);
	xmlhttp.send();
} 
</script>
</head>
<body>
<form>
<input type="text" id="feet-box">
<input type="button" value="convert" onclick="ajax();">
</form>
<div id="meter-box" style="background:#00ffff;"/>
</html>
