	__nest__ (
		__all__,
		'div_issues.issue387', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var div_issues = {};
					var __name__ = 'div_issues.issue387';
					__nest__ (div_issues, 'issue387.test1', __init__ (__world__.div_issues.issue387.test1));
					__nest__ (div_issues, 'issue387.test1.test2', __init__ (__world__.div_issues.issue387.test1.test2));
					var run387 = function (autoTester) {
						autoTester.check (div_issues.issue387.test1.getReport ());
						autoTester.check ('From test: ', div_issues.issue387.test1.test2.C.__module__);
						autoTester.check (__name__);
						var D = __class__ ('D', [object], {
							__module__: __name__,
						});
						autoTester.check ('From test:', D.__module__);
						autoTester.check (D.__name__);
					};
					__pragma__ ('<use>' +
						'div_issues.issue387.test1' +
						'div_issues.issue387.test1.test2' +
					'</use>')
					__pragma__ ('<all>')
						__all__.__name__ = __name__;
						__all__.run387 = run387;
					__pragma__ ('</all>')
				}
			}
		}
	);
