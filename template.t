<html>
<head>
<meta charset="utf-8">
<script>
'use strict';

const data = {{data}};

function mouseover(event) {
	const title = event.target.dataset['title'];
	document.getElementById('title').textContent = title;
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
			circle.setAttribute('cx', hw + 5 * data.x[i]);
			circle.setAttribute('cy', hh + 5 * data.y[i]);
			circle.setAttribute('r', 5);
			circle.setAttribute('opacity', 0.1);
			circle.dataset['title'] = data.titles[i];
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
<svg width="1000" height="1000" id="svg"></svg>
</body>
</html>
