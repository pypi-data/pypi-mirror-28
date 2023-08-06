	__nest__ (
		__all__,
		'modules.mod2.mod22', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'modules.mod2.mod22';
					var B = __class__ ('B', [object], {
						__module__: __name__,
						get __init__ () {return __get__ (this, function (self) {
							self.x = 'Geef mij maar Amsterdam\n';
						});}
					});
					__pragma__ ('<all>')
						__all__.B = B;
						__all__.__name__ = __name__;
					__pragma__ ('</all>')
				}
			}
		}
	);
