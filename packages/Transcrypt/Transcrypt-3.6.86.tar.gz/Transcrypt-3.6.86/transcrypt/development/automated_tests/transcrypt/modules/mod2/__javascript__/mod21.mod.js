	__nest__ (
		__all__,
		'modules.mod2.mod21', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'modules.mod2.mod21';
					var f = function () {
						return 'London is the town for me\n';
					};
					__pragma__ ('<all>')
						__all__.__name__ = __name__;
						__all__.f = f;
					__pragma__ ('</all>')
				}
			}
		}
	);
