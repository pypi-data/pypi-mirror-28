	__nest__ (
		__all__,
		'mod1', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'mod1';
					var test = function (i) {
						var a = 3;
						var a = 4.5;
						return str (i);
					};
					__pragma__ ('<all>')
						__all__.__name__ = __name__;
						__all__.test = test;
					__pragma__ ('</all>')
				}
			}
		}
	);
