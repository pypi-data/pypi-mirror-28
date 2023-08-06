	__nest__ (
		__all__,
		'color', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'color';
					var msgs = list ([]);
					var styles = list ([]);
					var debug = 0;
					var _recurse = function (col, g) {
						var s = tuple ([].slice.apply (arguments).slice (2));
						var __left0__ = g;
						var msgs = __left0__ [0];
						var styles = __left0__ [1];
						var hsl = __left0__ [2];
						var lu = tuple ([tuple (['color', 0]), tuple (['background-color', 1])]);
						var hsl = hsl [col];
						var hsl = list ([hsl.__getslice__ (0, 3, 1), list ([hsl [0], hsl [1], hsl [3]])]);
						var css = ';'.join ((function () {
							var __accu0__ = [];
							for (var [i, j] of lu) {
								__accu0__.append (str (i) + ': hsl({}, {}%, {}%)'.format (...hsl [j]));
							}
							return __accu0__;
						}) ());
						for (var i of s) {
							if (debug) {
								styles.append (col);
							}
							else {
								styles.append (css);
							}
							msgs.append ('%c');
							try {
								i (g);
							}
							catch (__except0__) {
								msgs.py_pop ();
								msgs.append ('%c{}'.format (i));
							}
						}
					};
					var hsl = dict ({'red': list ([0, 100, 90, 50]), 'orange': list ([39, 100, 85, 50]), 'yellow': list ([60, 100, 35, 50]), 'green': list ([120, 100, 60, 25]), 'blue': list ([240, 100, 90, 50]), 'purple': list ([300, 100, 85, 25]), 'black': list ([0, 0, 80, 0]), 'gray': list ([237, 8, 80, 50])});
					var _col = function (col) {
						return (function __lambda__ () {
							var parts = tuple ([].slice.apply (arguments).slice (0));
							return (function __lambda__ (g) {
								return _recurse (col, g, ...parts);
							});
						});
					};
					var colors = dict ({});
					for (var col of hsl.py_keys ()) {
						colors [col] = _col (col);
					}
					var cprint = function () {
						var s = tuple ([].slice.apply (arguments).slice (0));
						var __left0__ = tuple ([list ([]), list ([])]);
						var msgs = __left0__ [0];
						var styles = __left0__ [1];
						for (var i of s) {
							i (tuple ([msgs, styles, hsl]));
						}
						if (debug) {
							for (var i = 0; i < len (msgs); i++) {
								print (msgs [i], '-> ', styles [i]);
							}
						}
						else {
							var msg = ''.join (msgs);
							var st = '", "'.join (styles);
							var st = ''.join (tuple (['console.log("', msg, ('", "' + st) + '")']));
							eval(st)
						}
					};
					__pragma__ ('<all>')
						__all__.__name__ = __name__;
						__all__._col = _col;
						__all__._recurse = _recurse;
						__all__.col = col;
						__all__.colors = colors;
						__all__.cprint = cprint;
						__all__.debug = debug;
						__all__.hsl = hsl;
						__all__.msgs = msgs;
						__all__.styles = styles;
					__pragma__ ('</all>')
				}
			}
		}
	);
