	__nest__ (
		__all__,
		'div_issues.issue387.test1', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var div_issues = {};
					var __name__ = 'div_issues.issue387.test1';
					__nest__ (div_issues, 'issue387.test1.test2', __init__ (__world__.div_issues.issue387.test1.test2));
					var getReport = function () {
						return 'From test1: {}'.format (div_issues.issue387.test1.test2.C.__module__);
					};
					__pragma__ ('<use>' +
						'div_issues.issue387.test1.test2' +
					'</use>')
					__pragma__ ('<all>')
						__all__.__name__ = __name__;
						__all__.getReport = getReport;
					__pragma__ ('</all>')
				}
			}
		}
	);
