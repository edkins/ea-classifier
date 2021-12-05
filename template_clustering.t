<html>
<head>
<meta charset="utf-8">
<script>
"use strict";

const data = {{data}};

const colormap = [
	'#1f77b4',  // blue
	'#ff7f0e',  // orange
	'#2ca02c',  // green
	'#d62728',  // red
	'#9467bd',  // purple
	'#8c564b',  // brown
	'#e377c2',  // pink
	'#7f7f7f',  // grey
	'#bcbd22',  // olive
	'#17becf',  // cyan

	'#202080',  // indigo
	'#ffd000',  // gold
	'#006000',  // dark green
	'#c05020',  // brick red
	'#ff00a0',  // raspberry
	'#503000',  // red-brown
	'#ff00ff',  // magenta
	'#8080c0',  // blue-grey
	'#c0c090',  // beige
	'#00c090',  // turquoise
];

function mouseover(event) {
	const i = parseInt(event.target.dataset.i);
	show_info(i);
}

function show_info(i) {
	let title = `<b>${data.titles[i]}</b><br>`;
	document.getElementById('title').innerHTML = title;
}

let diagram = 0;
function show_cluster_diagram() {
	const svg = document.getElementById('svg');
	const hw = svg.getAttribute('width') / 2;
	const hh = svg.getAttribute('height') / 2;
	svg.innerHTML = '';
	for (let i = 0; i < data.x.length; i++) {
		const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
		rect.setAttribute('x', hw + 200 * data.x[i]);
		rect.setAttribute('y', hh + 200 * data.y[i]);
		rect.setAttribute('width', 3);
		rect.setAttribute('height', 3);
		rect.setAttribute('r', 3);
		rect.setAttribute('fill', '#000');
		rect.dataset.i = i;
		rect.onmouseover = mouseover;
		svg.appendChild(rect);
	}
}

function change_diagram() {
	diagram = (diagram + 1) % 1;
	show_diagram();
}

function show_diagram() {
	if (diagram === 0) {
		show_cluster_diagram();
	} else if (diagram === 1) {
		show_table_diagram();
	}
}

function load() {
	show_diagram();
	show_info(0);
}

window.onload = load;
</script>
</head>
<body>
<svg width="600" height="600" id="svg" style="position:absolute; left:1000px; top:0px" onmousedown="change_diagram()"></svg>
<div>
	<span id="title">&nbsp;</span>
</div>
</body>
</html>
