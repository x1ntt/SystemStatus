

function active_oled(active) {
	$.get('/api/update/oled?active='+active, function(res) {
		alert(res);
	});
}

$(document).ready(function() {
    function updatenode() {
        $.get('/api/get/all_node', function(nodes) {
            console.log(nodes);
            $("#status").text(JSON.stringify(nodes));
        });
    }

    // setInterval(updatenode, 1000);

})
