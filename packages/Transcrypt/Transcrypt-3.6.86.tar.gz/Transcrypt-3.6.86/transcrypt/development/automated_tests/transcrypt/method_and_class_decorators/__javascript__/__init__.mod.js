	__nest__ (
		__all__,
		'method_and_class_decorators', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'method_and_class_decorators';
					var run = function (autoTester) {
						var adecorator = __class__ ('adecorator', [object], {
							__module__: __name__,
							get __init__ () {return __get__ (this, function (self) {
								var kwargs = dict ();
								if (arguments.length) {
									var __ilastarg0__ = arguments.length - 1;
									if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
										var __allkwargs0__ = arguments [__ilastarg0__--];
										for (var __attrib0__ in __allkwargs0__) {
											switch (__attrib0__) {
												case 'self': var self = __allkwargs0__ [__attrib0__]; break;
												default: kwargs [__attrib0__] = __allkwargs0__ [__attrib0__];
											}
										}
										delete kwargs.__kwargtrans__;
									}
									var args = tuple ([].slice.apply (arguments).slice (1, __ilastarg0__ + 1));
								}
								else {
									var args = tuple ();
								}
								self.args = args;
								self.kwargs = kwargs;
							});},
							get __call__ () {return __get__ (this, function (self, func) {
								var wrapper = function () {
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
									var slf = args [0];
									var saved = dict ({});
									for (var [k, v] of self.kwargs.py_items ()) {
										if (hasattr (slf, k)) {
											saved [k] = getattr (slf, k);
											setattr (slf, k, v);
										}
									}
									var ret = func (...args, __kwargtrans__ (kwargs));
									for (var [k, v] of saved.py_items ()) {
										setattr (slf, k, v);
									}
									return ret;
								};
								return wrapper;
							});}
						});
						var method_decorator = function (prefix) {
							var inner_decorator = function (method) {
								var wrapper = function (self, py_name) {
									autoTester.check (py_name);
									return method (self, prefix + py_name);
								};
								return wrapper;
							};
							return inner_decorator;
						};
						var method_decorator2 = function (prefix) {
							var inner_decorator = function (method) {
								var wrapper = function (self, py_name) {
									autoTester.check (py_name);
									return method (self, prefix + py_name);
								};
								return wrapper;
							};
							return inner_decorator;
						};
						var multiplier = function (m) {
							var inner_decorator = function (method) {
								var wrapper = function (self, num) {
									autoTester.check (num);
									var n = method (self, num);
									return n * m;
								};
								return wrapper;
							};
							return inner_decorator;
						};
						var classmethod_decorator = function (method) {
							var wrapper = function (cls, a, b) {
								autoTester.check (cls.__name__, a, b);
								return method (cls, b, a);
							};
							return wrapper;
						};
						var class_decorator = function (prefix) {
							var wrapper = function (cls) {
								autoTester.check (prefix + cls.__name__);
								return cls;
							};
							return wrapper;
						};
						var MyClass = class_decorator ('outer_') ( __class__ ('MyClass', [object], {
							__module__: __name__,
							InnerClass: class_decorator ('inner_') ( __class__ ('InnerClass', [object], {
								__module__: __name__,
								get mymethod () {return __get__ (this, method_decorator ('inner_first_') (method_decorator2 ('inner_second_') (function (self, py_name) {
									autoTester.check (py_name);
								})));},
								get myclassmethod () {return __getcm__ (this, classmethod_decorator (function (cls, a, b) {
									autoTester.check (cls.__name__, a, b);
									return a + b;
								}));},
								get mystaticmethod () {return function (a, b) {
									autoTester.check (a, b);
									return a + b;
								};},
								get _get_inner_property () {return __get__ (this, function (self) {
									return 'I am a property';
								});}
							})),
							get __init__ () {return __get__ (this, function (self) {
								self.greetings = 'Hello';
							});},
							get get_greetings () {return __get__ (this, __call__ (__call__ (adecorator, null, __kwargtrans__ ({greetings: 'Goodbye'})), null, function (self) {
								return self.greetings;
							}));},
							get mymethod () {return __get__ (this, method_decorator ('first_') (method_decorator2 ('second_') (function (self, py_name) {
								autoTester.check (py_name);
							})));},
							get number () {return __get__ (this, multiplier (5) (function (self, num) {
								return num;
							}));},
							get myclassmethod () {return __getcm__ (this, function (cls, a, b) {
								autoTester.check (cls.__name__, a, b);
								return a + b;
							});},
							get mystaticmethod () {return function (a, b) {
								autoTester.check (a + b);
								return a + b;
							};},
							get _get_simple_property () {return __get__ (this, function (self) {
								return self.greetings;
							});},
							get _set_simple_property () {return __get__ (this, function (self, value) {
								self.greetings = value;
							});},
							get run () {return __get__ (this, function (self) {
								var inner_obj = self.InnerClass ();
								inner_obj.mymethod ('Dog');
								var result1 = inner_obj.myclassmethod ('param1', 'param2');
								var result2 = self.InnerClass.myclassmethod ('param1', 'param2');
								autoTester.check (result1 == result2);
								var result1 = inner_obj.mystaticmethod ('param1', 'param2');
								var result2 = self.InnerClass.mystaticmethod ('param1', 'param2');
								autoTester.check (result1 == result2);
								autoTester.check (inner_obj.inner_property);
							});}
						}));
						Object.defineProperty (MyClass, 'simple_property', property.call (MyClass, MyClass._get_simple_property, MyClass._set_simple_property));
						Object.defineProperty (MyClass.InnerClass, 'inner_property', property.call (MyClass.InnerClass, MyClass.InnerClass._get_inner_property));;
						var myobj = MyClass ();
						myobj.mymethod ('Cat');
						autoTester.check (myobj.greetings);
						autoTester.check (myobj.get_greetings ());
						var result1 = myobj.myclassmethod ('param1', 'param2');
						var result2 = MyClass.myclassmethod ('param1', 'param2');
						autoTester.check (result1 == result2);
						var result1 = myobj.mystaticmethod ('param1', 'param2');
						var result2 = MyClass.mystaticmethod ('param1', 'param2');
						autoTester.check (result1 == result2);
						autoTester.check (myobj.number (3));
						autoTester.check (myobj.simple_property);
						myobj.simple_property = 'New value';
						autoTester.check (myobj.simple_property);
						autoTester.check (myobj.greetings == myobj.simple_property);
						myobj.run ();
					};
					__pragma__ ('<all>')
						__all__.__name__ = __name__;
						__all__.run = run;
					__pragma__ ('</all>')
				}
			}
		}
	);
