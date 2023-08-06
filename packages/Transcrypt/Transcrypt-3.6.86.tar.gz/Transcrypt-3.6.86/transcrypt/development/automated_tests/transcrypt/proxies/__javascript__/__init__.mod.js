	__nest__ (
		__all__,
		'proxies', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'proxies';
					var run = function (autoTester) {
						var CodedStore = __class__ ('CodedStore', [object], {
							__module__: __name__,
							get __init__ () {return __get__ (this, function (self) {
								try {
									self ["__dict__"] = {}
								}
								catch (__except0__) {
									// pass;
								}
							});},
							get __setattr__ () {return __get__ (this, function (self, py_name, message) {
								self.__dict__ ['_' + py_name] = 'coded_' + message;
							});},
							get __getattr__ () {return __get__ (this, function (self, py_name) {
								return 'decoded_' + self.__dict__ ['_' + py_name];
							});},
							get peek () {return __get__ (this, function (self, py_name) {
								return self.__dict__ ['_' + py_name];
							});}
						});
						var s = CodedStore ();
						s.john = 'brown';
						s.mary = 'white';
						autoTester.check (s.peek ('john'));
						autoTester.check (s.peek ('mary'));
						autoTester.check (s.john);
						autoTester.check (s.mary);
						var A = __class__ ('A', [object], {
							__module__: __name__,
							get __init__ () {return __get__ (this, function (self) {
								self.p = 1;
								self.q = 2;
							});}
						});
						var B = __class__ ('B', [A], {
							__module__: __name__,
							get __getattr__ () {return __get__ (this, function (self, py_name) {
								return 'Faked {}'.format (py_name);
							});}
						});
						var C = __class__ ('C', [A], {
							__module__: __name__,
							get __setattr__ () {return __get__ (this, function (self, py_name, value) {
								autoTester.check ('Set faked {}'.format (py_name));
								A.__setattr__ (self, py_name, value);
							});}
						});
						var D = __class__ ('D', [B, C], {
							__module__: __name__,
						});
						var a = A ();
						var b = B ();
						var c = C ();
						var d = D ();
						autoTester.check (a.p, a.q);
						a.p = 3;
						autoTester.check (a.p, a.q);
						autoTester.check (b.p, b.q, b.r, b.s);
						b.p = 4;
						b.r = 5;
						autoTester.check (b.p, b.q, b.r, b.s);
						autoTester.check (c.p, c.q);
						c.p = 6;
						c.q = 7;
						autoTester.check (c.p, c.q);
						autoTester.check (d.p, d.q, d.r, d.s);
						d.p = 8;
						d.q = 9;
						d.r = 10;
						d.s = 11;
						autoTester.check (d.p, d.q, d.r, d.s);
					};
					__pragma__ ('<all>')
						__all__.__name__ = __name__;
						__all__.run = run;
					__pragma__ ('</all>')
				}
			}
		}
	);
