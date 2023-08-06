	__nest__ (
		__all__,
		'decorators', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'decorators';
					var run = function (autoTester) {
						var repeat3 = function (bareFunc) {
							var innerFunc = function () {
								var kwargs = dict ();
								if (arguments.length) {
									var __ilastarg0__ = arguments.length - 1;
									if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
										var __allkwargs0__ = arguments [__ilastarg0__--];
										for (var __attrib0__ in __allkwargs0__) {
											switch (__attrib0__) {
												default: kwargs [__attrib0__] = __allkwargs0__ [__attrib0__];
											}
										}
										delete kwargs.__kwargtrans__;
									}
									var args = tuple ([].slice.apply (arguments).slice (0, __ilastarg0__ + 1));
								}
								else {
									var args = tuple ();
								}
								autoTester.check ('BEGIN repeat3');
								for (var i = 0; i < 3; i++) {
									bareFunc (...args, __kwargtrans__ (kwargs));
								}
								autoTester.check ('END repeat3');
							};
							return innerFunc;
						};
						var repeatN = function (n) {
							var repeat = function (bareFunc) {
								var innerFunc = function () {
									var kwargs = dict ();
									if (arguments.length) {
										var __ilastarg0__ = arguments.length - 1;
										if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
											var __allkwargs0__ = arguments [__ilastarg0__--];
											for (var __attrib0__ in __allkwargs0__) {
												switch (__attrib0__) {
													default: kwargs [__attrib0__] = __allkwargs0__ [__attrib0__];
												}
											}
											delete kwargs.__kwargtrans__;
										}
										var args = tuple ([].slice.apply (arguments).slice (0, __ilastarg0__ + 1));
									}
									else {
										var args = tuple ();
									}
									autoTester.check ('BEGIN repeatN ({})'.format (n));
									for (var i = 0; i < n; i++) {
										bareFunc (...args, __kwargtrans__ (kwargs));
									}
									autoTester.check ('END repeatN ({})'.format (n));
								};
								return innerFunc;
							};
							return repeat;
						};
						var Repeater = __class__ ('Repeater', [object], {
							__module__: __name__,
							get __init__ () {return __get__ (this, function (self, n) {
								self.n = n;
							});},
							get __call__ () {return __get__ (this, function (self, bareFunc) {
								var innerFunc = function () {
									var kwargs = dict ();
									if (arguments.length) {
										var __ilastarg0__ = arguments.length - 1;
										if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
											var __allkwargs0__ = arguments [__ilastarg0__--];
											for (var __attrib0__ in __allkwargs0__) {
												switch (__attrib0__) {
													default: kwargs [__attrib0__] = __allkwargs0__ [__attrib0__];
												}
											}
											delete kwargs.__kwargtrans__;
										}
										var args = tuple ([].slice.apply (arguments).slice (0, __ilastarg0__ + 1));
									}
									else {
										var args = tuple ();
									}
									autoTester.check ('BEGIN repeat3');
									for (var i = 0; i < self.n; i++) {
										bareFunc (...args, __kwargtrans__ (kwargs));
									}
									autoTester.check ('END repeat3');
								};
								return innerFunc;
							});}
						});
						var funcNoArg = repeatN (4) (repeat3 (function () {
							autoTester.check ('spam');
						}));
						funcNoArg ();
						autoTester.check ();
						var funcArg = repeat3 (repeatN (2) (function (a) {
							if (arguments.length) {
								var __ilastarg0__ = arguments.length - 1;
								if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
									var __allkwargs0__ = arguments [__ilastarg0__--];
									for (var __attrib0__ in __allkwargs0__) {
										switch (__attrib0__) {
											case 'a': var a = __allkwargs0__ [__attrib0__]; break;
										}
									}
								}
							}
							else {
							}
							autoTester.check ('eggs', a);
						}));
						funcArg (3);
						autoTester.check ();
						funcArg (__kwargtrans__ ({a: 4}));
						autoTester.check ();
						var funcNoArg2 = __call__ (__call__ (Repeater, null, 3), null, function () {
							__call__ (autoTester.check, autoTester, 'toast');
						});
						funcNoArg2 ();
						autoTester.check ();
						var funcArg2 = __call__ (__call__ (Repeater, null, 5), null, function (a) {
							if (arguments.length) {
								var __ilastarg0__ = arguments.length - 1;
								if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
									var __allkwargs0__ = arguments [__ilastarg0__--];
									for (var __attrib0__ in __allkwargs0__) {
										switch (__attrib0__) {
											case 'a': var a = __allkwargs0__ [__attrib0__]; break;
										}
									}
								}
							}
							else {
							}
							__call__ (autoTester.check, autoTester, 'jam', a);
						});
						funcArg2 (3);
						autoTester.check ();
						funcArg2 (__kwargtrans__ ({a: 4}));
						autoTester.check ();
						var py_next = function (bareFunc) {
							var innerFunc = function (value) {
								return bareFunc (value + 1);
							};
							return innerFunc;
						};
						var Number = py_next ( __class__ ('Number', [object], {
							__module__: __name__,
							get __init__ () {return __get__ (this, function (self, value) {
								self.value = value;
							});}
						}));
						autoTester.check ('two', Number (1).value);
						var Test = __class__ ('Test', [object], {
							__module__: __name__,
							get f () {return __getcm__ (this, function (cls, x, y) {
								autoTester.check (cls.__name__, x, y);
							});},
							get g () {return __get__ (this, function (self, x, y) {
								autoTester.check (self.__class__.__name__, x, y);
							});}
						});
						var test = Test ();
						test.f (1, 2);
						test.g (3, 4);
					};
					__pragma__ ('<all>')
						__all__.__name__ = __name__;
						__all__.run = run;
					__pragma__ ('</all>')
				}
			}
		}
	);
