	__nest__ (
		__all__,
		'modules.mod1.mod11.mod111', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'modules.mod1.mod11.mod111';
					var A = __class__ ('A', [object], {
						__module__: __name__,
						get __init__ () {return __get__ (this, function (self, x) {
							self.x = x;
						});},
						get f () {return __get__ (this, function (self) {
							return self.x;
						});}
					});
					__pragma__ ('<all>')
						__all__.A = A;
						__all__.__name__ = __name__;
					__pragma__ ('</all>')
				}
			}
		}
	);
