<html>
<head>
<meta charset="utf-8">
<script>
'use strict';

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
	const i = parseInt(event.target.dataset['i']);
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

function load() {
	const text = false;
	const svg = document.getElementById('svg');
	const hw = svg.getAttribute('width') / 2;
	const hh = svg.getAttribute('height') / 2;
	console.log(hw, hh);
	for (let i = 0; i < data.x.length; i++) {
		if (text) {
			const t = document.createElementNS('http://www.w3.org/2000/svg', 'text');
			t.setAttribute('x', hw + 50 * data.x[i]);
			t.setAttribute('y', hh + 50 * data.y[i]);
			t.style.fontSize = 5;
			t.textContent = data.titles[i];
			svg.appendChild(t);
		} else {
			const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
			const am = argmax(data.topicality[i]);
			circle.setAttribute('cx', hw + 100 * data.x[i]);
			circle.setAttribute('cy', hh + 100 * data.y[i]);
			circle.setAttribute('r', 3);
			circle.setAttribute('opacity', Math.sqrt(data.topicality[i][am]));
			circle.setAttribute('fill', colormap[am % colormap.length]);
			circle.dataset['i'] = i;
			circle.onmouseover = mouseover;
			svg.appendChild(circle);
		}
	}
}

window.onload = load;
</script>
</head>
<body>
<div>
	<span id="title">&nbsp;</span>
</div>
<svg width="600" height="600" id="svg"></svg>
</body>
</html>
