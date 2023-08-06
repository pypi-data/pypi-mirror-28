	(function () {
		var __name__ = '__main__';
		var Turtle = __init__ (__world__.turtle).Turtle;
		var __name__ = __init__ (__world__.turtle).__name__;
		var _allTurtles = __init__ (__world__.turtle)._allTurtles;
		var _debug = __init__ (__world__.turtle)._debug;
		var _defaultElement = __init__ (__world__.turtle)._defaultElement;
		var _defaultTurtle = __init__ (__world__.turtle)._defaultTurtle;
		var _height = __init__ (__world__.turtle)._height;
		var _ns = __init__ (__world__.turtle)._ns;
		var _offset = __init__ (__world__.turtle)._offset;
		var _rightSize = __init__ (__world__.turtle)._rightSize;
		var _svg = __init__ (__world__.turtle)._svg;
		var _timer = __init__ (__world__.turtle)._timer;
		var _width = __init__ (__world__.turtle)._width;
		var abs = __init__ (__world__.turtle).abs;
		var back = __init__ (__world__.turtle).back;
		var begin_fill = __init__ (__world__.turtle).begin_fill;
		var bgcolor = __init__ (__world__.turtle).bgcolor;
		var circle = __init__ (__world__.turtle).circle;
		var color = __init__ (__world__.turtle).color;
		var distance = __init__ (__world__.turtle).distance;
		var done = __init__ (__world__.turtle).done;
		var down = __init__ (__world__.turtle).down;
		var end_fill = __init__ (__world__.turtle).end_fill;
		var forward = __init__ (__world__.turtle).forward;
		var goto = __init__ (__world__.turtle).goto;
		var home = __init__ (__world__.turtle).home;
		var left = __init__ (__world__.turtle).left;
		var ontimer = __init__ (__world__.turtle).ontimer;
		var pensize = __init__ (__world__.turtle).pensize;
		var pos = __init__ (__world__.turtle).pos;
		var position = __init__ (__world__.turtle).position;
		var py_clear = __init__ (__world__.turtle).py_clear;
		var reset = __init__ (__world__.turtle).reset;
		var right = __init__ (__world__.turtle).right;
		var setDefaultElement = __init__ (__world__.turtle).setDefaultElement;
		var speed = __init__ (__world__.turtle).speed;
		var up = __init__ (__world__.turtle).up;
		bgcolor ('black');
		for (var [a_color, a_pensize, start_radius, stop_radius, radius_step] of tuple ([tuple (['green', 1, 82, 40, -(6)]), tuple (['red', 1, 84, 40, -(6)]), tuple (['white', 2, 98, 50, -(5)]), tuple (['yellow', 2, 70, 50, -(5)]), tuple (['blue', 2, 97, 70, -(5)]), tuple (['orange', 2, 87, 40, -(17)]), tuple (['pink', 3, 102, 60, -(17)])])) {
			pensize (a_pensize);
			color (a_color);
			for (var angle_index = 0; angle_index < 10; angle_index++) {
				for (var radius of range (start_radius, stop_radius, radius_step)) {
					circle (radius);
				}
				right (36);
			}
		}
		done ();
		__pragma__ ('<use>' +
			'turtle' +
		'</use>')
		__pragma__ ('<all>')
			__all__.Turtle = Turtle;
			__all__.__name__ = __name__;
			__all__._allTurtles = _allTurtles;
			__all__._debug = _debug;
			__all__._defaultElement = _defaultElement;
			__all__._defaultTurtle = _defaultTurtle;
			__all__._height = _height;
			__all__._ns = _ns;
			__all__._offset = _offset;
			__all__._rightSize = _rightSize;
			__all__._svg = _svg;
			__all__._timer = _timer;
			__all__._width = _width;
			__all__.a_color = a_color;
			__all__.a_pensize = a_pensize;
			__all__.abs = abs;
			__all__.angle_index = angle_index;
			__all__.back = back;
			__all__.begin_fill = begin_fill;
			__all__.bgcolor = bgcolor;
			__all__.circle = circle;
			__all__.color = color;
			__all__.distance = distance;
			__all__.done = done;
			__all__.down = down;
			__all__.end_fill = end_fill;
			__all__.forward = forward;
			__all__.goto = goto;
			__all__.home = home;
			__all__.left = left;
			__all__.ontimer = ontimer;
			__all__.pensize = pensize;
			__all__.pos = pos;
			__all__.position = position;
			__all__.py_clear = py_clear;
			__all__.radius = radius;
			__all__.radius_step = radius_step;
			__all__.reset = reset;
			__all__.right = right;
			__all__.setDefaultElement = setDefaultElement;
			__all__.speed = speed;
			__all__.start_radius = start_radius;
			__all__.stop_radius = stop_radius;
			__all__.up = up;
		__pragma__ ('</all>')
	}) ();
