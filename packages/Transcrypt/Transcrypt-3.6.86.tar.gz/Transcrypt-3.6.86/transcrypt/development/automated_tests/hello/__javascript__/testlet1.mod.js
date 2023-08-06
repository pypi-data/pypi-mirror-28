	__nest__ (
		__all__,
		'testlet1', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'testlet1';
					var run = function (autoTester) {
						autoTester.check ('goodbye');
						autoTester.check ('moon');
					};
					__pragma__ ('<all>')
						__all__.__name__ = __name__;
						__all__.run = run;
					__pragma__ ('</all>')
				}
			}
		}
	);
