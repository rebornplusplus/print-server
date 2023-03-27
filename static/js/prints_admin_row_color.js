function colorRow () {
	table = document.getElementById("result_list");
	for (var i = 1; i < table.rows.length; i++) {
		row = table.rows[i];
		val = row.cells[6].childNodes[0].value;
		if (val == 1) // queued
			row.classList.add("alert","alert-danger");
		else if(val == 2) // printing
			row.classList.add("alert","alert-warning");
		else
			row.classList.add("alert","alert-success");
	}
}
// call functoin when document is ready
document.addEventListener("DOMContentLoaded", colorRow);