	(function () {
		var itertools = {};
		var math = {};
		var random = {};
		var __name__ = '__main__';
		__nest__ (random, '', __init__ (__world__.random));
		__nest__ (math, '', __init__ (__world__.math));
		__nest__ (itertools, '', __init__ (__world__.itertools));
		var xValues = (function () {
			var __accu0__ = [];
			for (var step = 0; step < 201; step++) {
				__accu0__.append (((2 * math.pi) * step) / 200);
			}
			return __accu0__;
		}) ();
		var yValuesList = list ([(function () {
			var __accu0__ = [];
			for (var xValue of xValues) {
				__accu0__.append (math.sin (xValue) + 0.5 * math.sin (xValue * 3 + 0.25 * math.sin (xValue * 5)));
			}
			return __accu0__;
		}) (), (function () {
			var __accu0__ = [];
			for (var xValue of xValues) {
				__accu0__.append ((xValue <= math.pi ? 1 : -(1)));
			}
			return __accu0__;
		}) ()]);
		var kind = 'linear';
		Plotly.plot (kind, (function () {
			var __accu0__ = [];
			for (var yValues of yValuesList) {
				__accu0__.append (dict ({x: xValues, y: yValues}));
			}
			return __accu0__;
		}) (), dict ({title: kind, xaxis: dict ({title: 'U (t) [V]'}), yaxis: dict ({title: 't [s]'})}));
		try {
			var xValues = list (range (10));
			var yValues = (function () {
				var __accu0__ = [];
				for (var x of xValues) {
					__accu0__.append (math.exp (Math.pow (x, 2)));
				}
				return __accu0__;
			}) ();
			var kind = 'logarithmic';
			Plotly.plot (kind, list ([dict ({x: xValues, y: yValues})]), dict ({title: kind, xaxis: dict ({title: 'x'}), yaxis: dict ({type: 'log', tickformat: '2e', title: 'exp (x**2)'})}));
		}
		catch (__except0__) {
			// pass;
		}
		var tangentialValues = list (range (-(180), 180));
		var radialValuesList = list ([(function () {
			var __accu0__ = [];
			for (var t of tangentialValues) {
				__accu0__.append (abs (t));
			}
			return __accu0__;
		}) (), (function () {
			var __accu0__ = [];
			for (var t of tangentialValues) {
				__accu0__.append (180 - abs (t));
			}
			return __accu0__;
		}) (), (function () {
			var __accu0__ = [];
			for (var t of tangentialValues) {
				__accu0__.append (abs (2 * t));
			}
			return __accu0__;
		}) ()]);
		var kind = 'polar';
		Plotly.plot (kind, (function () {
			var __accu0__ = [];
			for (var [i, radialValues] of enumerate (radialValuesList)) {
				__accu0__.append (dict ({t: tangentialValues, r: radialValues, name: 'Cardioid {}'.format (i)}));
			}
			return __accu0__;
		}) (), dict ({title: kind}));
		var denseGrid = (function () {
			var __accu0__ = [];
			for (var step = -(100); step < 101; step++) {
				__accu0__.append (((8 * math.pi) * step) / 200);
			}
			return __accu0__;
		}) ();
		var sparseGrid = (function () {
			var __accu0__ = [];
			for (var step = -(100); step < 101; step += 10) {
				__accu0__.append (((8 * math.pi) * step) / 200);
			}
			return __accu0__;
		}) ();
		var getZValues = function (xGrid, yGrid) {
			return (function () {
				var __accu0__ = [];
				for (var y of yGrid) {
					__accu0__.append ((function () {
						var __accu1__ = [];
						for (var r of (function () {
							var __accu2__ = [];
							for (var x of xGrid) {
								__accu2__.append (math.sqrt (x * x + y * y));
							}
							return __accu2__;
						}) ()) {
							__accu1__.append (math.sin (r) / r);
						}
						return __accu1__;
					}) ());
				}
				return __accu0__;
			}) ();
		};
		var kind = 'wireframe';
		document.getElementById (kind).innerHTML = 'Plotly {} not yet functional for JS6'.format (kind);
		var kind = 'ribbon';
		Plotly.plot (kind, (function () {
			var __accu0__ = [];
			for (var i = 0; i < 10; i++) {
				__accu0__.append (dict ({x: denseGrid, y: list (range (i * 20, (i + 0.7) * 20)), z: getZValues (denseGrid, denseGrid).__getslice__ (i * 20, (i + 0.7) * 20, 1), type: 'surface', zmin: -(0.2), zmax: 1, showscale: !(i)}));
			}
			return __accu0__;
		}) (), dict ({title: kind}));
		var kind = 'surface';
		Plotly.plot (kind, list ([dict ({x: denseGrid, y: denseGrid, z: getZValues (denseGrid, denseGrid), type: kind, zmin: -(0.2), zmax: 1})]), dict ({title: kind}));
		var labels = list (['much', 'more', 'most']);
		var kind = 'bar';
		Plotly.plot (kind, list ([dict ({name: 'rare', x: labels, y: list ([1, 2, 4]), type: kind}), dict ({name: 'common', x: labels, y: list ([8, 16, 32]), type: kind})]), dict ({title: kind, barmode: 'group'}));
		var kind = 'pie';
		Plotly.plot (kind, list ([dict ({values: list ([1, 2, 3, 4, 5, 6]), labels: list (['least', 'less', 'little', 'much', 'more', 'most']), type: kind})]), dict ({title: kind}));
		var kind = 'scatter3d';
		var getRandoms = function (aMax) {
			return (function () {
				var __accu0__ = [];
				for (var i = 0; i < 20; i++) {
					__accu0__.append (random.randint (0, aMax));
				}
				return __accu0__;
			}) ();
		};
		Plotly.plot (kind, (function () {
			var __accu0__ = [];
			for (var aMax of tuple ([2, 5, 10])) {
				__accu0__.append (dict ({x: getRandoms (aMax), y: getRandoms (aMax), z: getRandoms (aMax), mode: 'markers', marker: dict ({color: 'rgb({}, 127, {})'.format (127 - aMax * 12, aMax * 12), size: 12, symbol: 'circle', line: dict ({color: 'rgb({}, 255, {})'.format (255 - aMax * 25, aMax * 25), width: 1})}), type: kind}));
			}
			return __accu0__;
		}) (), dict ({title: kind}));
		__pragma__ ('<use>' +
			'itertools' +
			'math' +
			'random' +
		'</use>')
		__pragma__ ('<all>')
			__all__.__name__ = __name__;
			__all__.denseGrid = denseGrid;
			__all__.getRandoms = getRandoms;
			__all__.getZValues = getZValues;
			__all__.kind = kind;
			__all__.labels = labels;
			__all__.radialValuesList = radialValuesList;
			__all__.sparseGrid = sparseGrid;
			__all__.tangentialValues = tangentialValues;
			__all__.xValues = xValues;
			__all__.yValues = yValues;
			__all__.yValuesList = yValuesList;
		__pragma__ ('</all>')
	}) ();
