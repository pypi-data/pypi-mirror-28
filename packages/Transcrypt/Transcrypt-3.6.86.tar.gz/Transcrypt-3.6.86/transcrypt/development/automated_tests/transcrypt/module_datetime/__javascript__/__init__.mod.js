	__nest__ (
		__all__,
		'module_datetime', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'module_datetime';
					var date = __init__ (__world__.datetime).date;
					var timedelta = __init__ (__world__.datetime).timedelta;
					var datetime = __init__ (__world__.datetime).datetime;
					var timezone = __init__ (__world__.datetime).timezone;
					var fix_time = function (dt) {
						if (__gt__ (dt.hour, 23)) {
							var dt = __sub__ (dt, __call__ (timedelta, null, __kwargtrans__ ({minutes: 60})));
						}
						if (__gt__ (dt.minute, 50)) {
							var dt = __sub__ (dt, __call__ (timedelta, null, __kwargtrans__ ({minutes: 10})));
						}
						return dt;
					};
					var run = function (autoTester) {
						var tz = timezone.utc;
						__call__ (autoTester.check, autoTester, __call__ (repr, null, tz));
						var tz2 = __call__ (timezone, null, __call__ (timedelta, null, __kwargtrans__ ({hours: __neg__ (5)})), 'EST');
						__call__ (autoTester.check, autoTester, __call__ (repr, null, tz2));
						var now = __call__ (fix_time, null, __call__ (datetime.utcnow, datetime));
						var now2 = __call__ (fix_time, null, __call__ (datetime.now, datetime, timezone.utc));
						__call__ (autoTester.check, autoTester, __eq__ (now.day, now2.day));
						__call__ (autoTester.check, autoTester, __eq__ (now.hour, now2.hour));
						__call__ (autoTester.check, autoTester, __call__ (__call__ (now.py_replace, now, __kwargtrans__ ({tzinfo: timezone.utc})).astimezone, __call__ (now.py_replace, now, __kwargtrans__ ({tzinfo: timezone.utc})), __kwargtrans__ ({tz: null})).hour);
						var delta = __call__ (timedelta, null, __kwargtrans__ ({days: 8, minutes: 15, microseconds: 685}));
						var delta2 = __call__ (timedelta, null, __kwargtrans__ ({days: 8, minutes: 15, microseconds: 684}));
						__call__ (autoTester.check, autoTester, delta);
						__call__ (autoTester.check, autoTester, delta2);
						__call__ (autoTester.check, autoTester, __eq__ (delta, delta2));
						__call__ (autoTester.check, autoTester, __gt__ (delta, delta2));
						__call__ (autoTester.check, autoTester, __lt__ (delta, delta2));
						var d = __call__ (date, null, 2017, 5, 5);
						__call__ (autoTester.check, autoTester, d.day);
						var d = __call__ (date.today, date);
						__call__ (autoTester.check, autoTester, d);
						__call__ (autoTester.check, autoTester, d.day);
						__call__ (autoTester.check, autoTester, __call__ (d.weekday, d));
						__call__ (autoTester.check, autoTester, __call__ (d.isoweekday, d));
						__call__ (autoTester.check, autoTester, __call__ (d.isocalendar, d));
						__call__ (autoTester.check, autoTester, __call__ (d.ctime, d));
						var d = __call__ (d.py_replace, d, __kwargtrans__ ({day: 28}));
						__call__ (autoTester.check, autoTester, d.day);
						__call__ (autoTester.check, autoTester, __call__ (d.strftime, d, '%Y.%m.%d'));
						__call__ (autoTester.check, autoTester, __call__ (d.ctime, d));
						__call__ (autoTester.check, autoTester, __call__ (d.isoformat, d));
						var d2 = __add__ (d, delta);
						var d3 = __sub__ (d2, delta);
						__call__ (autoTester.check, autoTester, d);
						__call__ (autoTester.check, autoTester, d2);
						__call__ (autoTester.check, autoTester, d3);
						__call__ (autoTester.check, autoTester, __eq__ (d, d3));
						__call__ (autoTester.check, autoTester, __gt__ (d, d3));
						__call__ (autoTester.check, autoTester, __lt__ (d, d3));
						__call__ (autoTester.check, autoTester, __eq__ (d, d2));
						__call__ (autoTester.check, autoTester, __gt__ (d, d2));
						__call__ (autoTester.check, autoTester, __lt__ (d, d2));
						var now = __call__ (fix_time, null, __call__ (datetime.now, datetime));
						__call__ (autoTester.check, autoTester, now.day);
						__call__ (autoTester.check, autoTester, now.hour);
						__call__ (autoTester.check, autoTester, (__add__ (now, __call__ (timedelta, null, __kwargtrans__ ({days: 2})))).day);
						var d = __call__ (datetime, null, 2010, 1, 1, __kwargtrans__ ({tzinfo: timezone.utc}));
						__call__ (autoTester.check, autoTester, d);
						var d = __call__ (datetime, null, 2017, 9, 19, 15, 43, 8, 142);
						__call__ (autoTester.check, autoTester, d);
						__call__ (autoTester.check, autoTester, __sub__ (d, __call__ (timedelta, null, __kwargtrans__ ({minutes: 150}))));
						var d = __call__ (datetime.strptime, datetime, '2017-03-14 15:28:14', '%Y-%m-%d %H:%M:%S');
						__call__ (autoTester.check, autoTester, d);
						__call__ (autoTester.check, autoTester, __call__ (d.strftime, d, '%Y.%m.%d %H:%M:%S'));
						var d = __add__ (d, __call__ (timedelta, null, __kwargtrans__ ({hours: 5, minutes: 18, seconds: 25})));
						__call__ (autoTester.check, autoTester, __call__ (d.strftime, d, '%Y-%m-%d %H:%M:%S'));
						var d = __call__ (d.py_replace, d, __kwargtrans__ ({year: 2016, month: 1}));
						__call__ (autoTester.check, autoTester, __call__ (d.ctime, d));
						__call__ (autoTester.check, autoTester, __call__ (d.isoformat, d));
						__call__ (autoTester.check, autoTester, __call__ (d.date, d));
						__call__ (autoTester.check, autoTester, __call__ (d.time, d));
						__call__ (autoTester.check, autoTester, __call__ (tuple, null, __call__ (d.timetuple, d)));
						__call__ (autoTester.check, autoTester, __call__ (tuple, null, __call__ (d.utctimetuple, d)));
						var d2 = __add__ (d, delta);
						var d3 = __sub__ (d2, delta);
						__call__ (autoTester.check, autoTester, d);
						__call__ (autoTester.check, autoTester, d2);
						__call__ (autoTester.check, autoTester, d3);
						__call__ (autoTester.check, autoTester, __eq__ (d, d3));
						__call__ (autoTester.check, autoTester, __gt__ (d, d3));
						__call__ (autoTester.check, autoTester, __lt__ (d, d3));
						__call__ (autoTester.check, autoTester, __eq__ (d, d2));
						__call__ (autoTester.check, autoTester, __gt__ (d, d2));
						__call__ (autoTester.check, autoTester, __lt__ (d, d2));
					};
					__pragma__ ('<use>' +
						'datetime' +
					'</use>')
					__pragma__ ('<all>')
						__all__.__name__ = __name__;
						__all__.date = date;
						__all__.datetime = datetime;
						__all__.fix_time = fix_time;
						__all__.run = run;
						__all__.timedelta = timedelta;
						__all__.timezone = timezone;
					__pragma__ ('</all>')
				}
			}
		}
	);
