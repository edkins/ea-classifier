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
	const am = argmax(data.topicality[i]);
	for (let j = 0; j < data.topicality[i].length; j++) {
		let topicality = data.topicality[i][j];
		let topic_name = data.topics[j].map(x=>x[0]).join(' ');
		let color = colormap[j % colormap.length];
		title += `<span style="color: ${color}">${topicality.toFixed(3)}</span>:`;
		if (j === am) {
			title += `<b>${topic_name}</b><br>`;
		} else {
			title += `${topic_name}<br>`;
		}
	}
	document.getElementById('title').innerHTML = title;
}

function highlight_two(j0,j1,value) {
	let title = `${value}<br>`;
	for (let j = 0; j < data.topicality[0].length; j++) {
		let topic_name = data.topics[j].map(x=>x[0]).join(' ');
		let color = colormap[j % colormap.length];
		if (j === j0 || j === j1) {
			title += `<b>${topic_name}</b><br>`;
		} else {
			title += `${topic_name}<br>`;
		}
	}
	document.getElementById('title').innerHTML = title;
}

function argmax(a) {
	let result = 0;
	let max = a[0];
	for (let i = 1; i < a.length; i++) {
		if (a[i] > max) {
			result = i;
			max = a[i];
		}
	}
	return result;
}

let diagram = 0;
function show_cluster_diagram() {
	const svg = document.getElementById('svg');
	const hw = svg.getAttribute('width') / 2;
	const hh = svg.getAttribute('height') / 2;
	svg.innerHTML = '';
	for (let i = 0; i < data.x.length; i++) {
		const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
		const am = argmax(data.topicality[i]);
		circle.setAttribute('cx', hw + 100 * data.x[i]);
		circle.setAttribute('cy', hh + 100 * data.y[i]);
		circle.setAttribute('r', 3);
		circle.setAttribute('opacity', Math.sqrt(data.topicality[i][am]));
		circle.setAttribute('fill', colormap[am % colormap.length]);
		circle.dataset.i = i;
		circle.onmouseover = mouseover;
		svg.appendChild(circle);
	}
}

function show_table_diagram() {
	const svg = document.getElementById('svg');
	const hw = svg.getAttribute('width') / 2;
	const hh = svg.getAttribute('height') / 2;
	svg.innerHTML = '';
	const n_topics = data.topics.length;
	const relatedness = new Float32Array(n_topics * n_topics);
	for (let i = 0; i < data.x.length; i++) {
		for (let j = 0; j < n_topics; j++) {
			for (let k = 0; k < n_topics; k++) {
				relatedness[n_topics * j + k] += data.topicality[i][j] * data.topicality[i][k];
			}
		}
	}
	for (let j = 0; j < n_topics; j++) {
		for (let k = 0; k < n_topics; k++) {
			const rect = document.createElementNS('http://www.w3.org/2000/svg', 'rect');
			const value = 10000 * relatedness[n_topics * j + k] * relatedness[n_topics * j + k] / relatedness[n_topics * j + j] / relatedness[n_topics * k + k];
			rect.setAttribute('x', 10 * j);
			rect.setAttribute('y', 10 * k);
			rect.setAttribute('width', 10);
			rect.setAttribute('height', 10);
			rect.setAttribute('stroke', '#000');
			rect.setAttribute('stroke-width', 1);
			rect.setAttribute('fill', `rgb(${value},${value},${value}`);
			rect.dataset.j = j;
			rect.dataset.k = k;
			rect.dataset.value = value;
			rect.onmouseover = mouseover_rect;
			svg.appendChild(rect);
		}
	}
}

function mouseover_rect(event) {
	const j = parseInt(event.target.dataset.j);
	const k = parseInt(event.target.dataset.k);
	highlight_two(j, k, event.target.dataset.value);
}

function change_diagram() {
	diagram = (diagram + 1) % 2;
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
