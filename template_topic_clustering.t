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
	event.target.setAttribute('fill','#f00');
	show_info(i);

	for (let j = 0; j < data.topics.length; j++) {
		const elem = document.getElementById(`text${j}`);
		let color = undefined;
		if (j === i) {
			color = '#f00';
		} else {
			color = `rgb(0,${1000 * data.relatedness[i][j]},0)`;
		}
		elem.setAttribute('fill', color);
	}
}

function show_info(i) {
	const topic_title = data.topics[i].map(t => t[0]).join(' ');
	let title = '';
	for (let t of data.topics[i]) {
		title += `<span style="opacity:${t[1]}">${t[0]}</span> `;
	}
	`<b>${topic_title}</b><br>`;
	document.getElementById('title').innerHTML = title;

	let listing = '';
	const articles = [];
	for (let j = 0; j < data.titles.length; j++) {
		const topicality = data.topicality[j][i];
		if (topicality > 0.01) {
			articles.push([topicality, data.titles[j]]);
		}
	}
	articles.sort((a,b) => b[0] - a[0]);
	for (let a of articles) {
		listing += `<span style="opacity: ${a[0]*5}">${a[1]}</span><br>`;
	}
	document.getElementById('article_listing').innerHTML = listing;
}

let diagram = 0;
function show_cluster_diagram() {
	const svg = document.getElementById('svg');
	const hw = svg.getAttribute('width') / 2;
	const hh = svg.getAttribute('height') / 2;
	svg.innerHTML = '';
	for (let i = 0; i < data.x.length; i++) {
		const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
		text.id = `text${i}`;
		text.setAttribute('x', hw + 250 * data.x[i]);
		text.setAttribute('y', hh + 250 * data.y[i]);
		text.setAttribute('fill', '#000');
		text.setAttribute('font-size', 10);
		text.textContent = data.topics[i][0][0];
		text.dataset.i = i;
		text.onmouseover = mouseover;
		svg.appendChild(text);
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
<svg width="1000" height="800" id="svg" style="position:absolute; left:0px; top:0px" onmousedown="change_diagram()"></svg>
<div>
	<span id="title">&nbsp;</span>
</div>
<div style="position:absolute; left:1000px; top:100px" id="article_listing">
</div>
</body>
</html>
