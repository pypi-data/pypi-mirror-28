	__nest__ (
		__all__,
		'warnings', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var re = {};
					var __name__ = 'warnings';
					__nest__ (re, '', __init__ (__world__.re));
					var Actions = __class__ ('Actions', [object], {
						__module__: __name__,
						error: 'error',
						ignore: 'ignore',
						always: 'always',
						defaultact: 'default',
						module: 'module',
						once: 'once'
					});
					var ActionSet = set ((function () {
						var __accu0__ = [];
						for (var x of dir (Actions)) {
							if (!(x.startswith ('_'))) {
								__accu0__.append (x);
							}
						}
						return __accu0__;
					}) ());
					var CategoryMap = dict ({'UserWarning': UserWarning, 'DeprecationWarning': DeprecationWarning, 'RuntimeWarning': RuntimeWarning});
					var _warnings_defaults = false;
					var filters = list ([]);
					var defaultaction = Actions.defaultact;
					var onceregistry = dict ({});
					var _filters_version = 1;
					var _filters_mutated = function () {
						_filters_version++;
					};
					var showwarning = function (message, category, filename, lineno, file, line) {
						if (typeof file == 'undefined' || (file != null && file .hasOwnProperty ("__kwargtrans__"))) {;
							var file = null;
						};
						if (typeof line == 'undefined' || (line != null && line .hasOwnProperty ("__kwargtrans__"))) {;
							var line = null;
						};
						var msg = WarningMessage (message, category, filename, lineno, file, line);
						_showwarnmsg_impl (msg);
					};
					var formatwarning = function (message, category, filename, lineno, line) {
						if (typeof line == 'undefined' || (line != null && line .hasOwnProperty ("__kwargtrans__"))) {;
							var line = null;
						};
						var msg = WarningMessage (message, category, filename, lineno, null, line);
						return _formatwarnmsg_impl (msg);
					};
					var _showwarnmsg_impl = function (msg) {
						var f = msg.file;
						var text = _formatwarnmsg (msg);
						if (f === null) {
							var text = text.rstrip ('\r\n');
							console.log (text);
						}
						else {
							try {
								f.write (text);
							}
							catch (__except0__) {
								if (isinstance (__except0__, Exception)) {
									var exc = __except0__;
									// pass;
								}
								else {
									throw __except0__;
								}
							}
						}
					};
					var _formatwarnmsg_impl = function (msg) {
						var s = '{}:{}: {}: {}\n'.format (msg.filename, msg.lineno, msg.category, str (msg.message));
						if (msg.line) {
							var line = msg.line.strip ();
							s += '  {}\n'.format (line);
						}
						return s;
					};
					var _showwarning = showwarning;
					var setShowWarning = function (func) {
						if (!(callable (func))) {
							var __except0__ = py_TypeError ('showwarning method must be callable');
							__except0__.__cause__ = null;
							throw __except0__;
						}
						showwarning = func;
					};
					var _showwarnmsg = function (msg) {
						if (!(callable (showwarning))) {
							var __except0__ = py_TypeError ('warnings.showwarning() must be set to a function or method');
							__except0__.__cause__ = null;
							throw __except0__;
						}
						showwarning (msg.message, msg.category, msg.filename, msg.lineno, msg.file, msg.line);
					};
					var _formatwarning = formatwarning;
					var _formatwarnmsg = function (msg) {
						if (formatwarning !== _formatwarning) {
							return formatwarning (msg.message, msg.category, msg.filename, msg.lineno, __kwargtrans__ ({line: msg.line}));
						}
						return _formatwarnmsg_impl (msg);
					};
					var addWarningCategory = function (cat) {
						var py_name = cat.__name__;
						if (!__in__ (py_name, CategoryMap)) {
							CategoryMap [py_name] = cat;
						}
						else {
							var __except0__ = Exception ('Warning Category {} already exists'.format (py_name));
							__except0__.__cause__ = null;
							throw __except0__;
						}
					};
					var filterwarnings = function (action, message, category, module, lineno, append) {
						if (typeof message == 'undefined' || (message != null && message .hasOwnProperty ("__kwargtrans__"))) {;
							var message = '';
						};
						if (typeof category == 'undefined' || (category != null && category .hasOwnProperty ("__kwargtrans__"))) {;
							var category = Warning;
						};
						if (typeof module == 'undefined' || (module != null && module .hasOwnProperty ("__kwargtrans__"))) {;
							var module = '';
						};
						if (typeof lineno == 'undefined' || (lineno != null && lineno .hasOwnProperty ("__kwargtrans__"))) {;
							var lineno = 0;
						};
						if (typeof append == 'undefined' || (append != null && append .hasOwnProperty ("__kwargtrans__"))) {;
							var append = false;
						};
						if (arguments.length) {
							var __ilastarg0__ = arguments.length - 1;
							if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
								var __allkwargs0__ = arguments [__ilastarg0__--];
								for (var __attrib0__ in __allkwargs0__) {
									switch (__attrib0__) {
										case 'action': var action = __allkwargs0__ [__attrib0__]; break;
										case 'message': var message = __allkwargs0__ [__attrib0__]; break;
										case 'category': var category = __allkwargs0__ [__attrib0__]; break;
										case 'module': var module = __allkwargs0__ [__attrib0__]; break;
										case 'lineno': var lineno = __allkwargs0__ [__attrib0__]; break;
										case 'append': var append = __allkwargs0__ [__attrib0__]; break;
									}
								}
							}
						}
						else {
						}
						assert (__in__ (action, ActionSet), 'invalid action: {}'.format (action));
						assert (isinstance (message, str), 'message must be a string');
						assert (isinstance (module, str), 'module must be a string');
						assert (isinstance (lineno, int) && lineno >= 0, 'lineno must be an int >= 0');
						_add_filter (action, re.compile (message, re.I), category, re.compile (module), lineno, __kwargtrans__ ({append: append}));
					};
					var simplefilter = function (action, category, lineno, append) {
						if (typeof category == 'undefined' || (category != null && category .hasOwnProperty ("__kwargtrans__"))) {;
							var category = Warning;
						};
						if (typeof lineno == 'undefined' || (lineno != null && lineno .hasOwnProperty ("__kwargtrans__"))) {;
							var lineno = 0;
						};
						if (typeof append == 'undefined' || (append != null && append .hasOwnProperty ("__kwargtrans__"))) {;
							var append = false;
						};
						if (arguments.length) {
							var __ilastarg0__ = arguments.length - 1;
							if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
								var __allkwargs0__ = arguments [__ilastarg0__--];
								for (var __attrib0__ in __allkwargs0__) {
									switch (__attrib0__) {
										case 'action': var action = __allkwargs0__ [__attrib0__]; break;
										case 'category': var category = __allkwargs0__ [__attrib0__]; break;
										case 'lineno': var lineno = __allkwargs0__ [__attrib0__]; break;
										case 'append': var append = __allkwargs0__ [__attrib0__]; break;
									}
								}
							}
						}
						else {
						}
						assert (__in__ (action, ActionSet), 'invalid action: {}'.format (action));
						assert (isinstance (lineno, int) && lineno >= 0, 'lineno must be an int >= 0');
						_add_filter (action, null, category, null, lineno, __kwargtrans__ ({append: append}));
					};
					var _add_filter = function () {
						if (arguments.length) {
							var __ilastarg0__ = arguments.length - 1;
							if (arguments [__ilastarg0__] && arguments [__ilastarg0__].hasOwnProperty ("__kwargtrans__")) {
								var __allkwargs0__ = arguments [__ilastarg0__--];
								for (var __attrib0__ in __allkwargs0__) {
									switch (__attrib0__) {
										case 'append': var append = __allkwargs0__ [__attrib0__]; break;
									}
								}
							}
							var item = tuple ([].slice.apply (arguments).slice (0, __ilastarg0__ + 1));
						}
						else {
							var item = tuple ();
						}
						if (!(append)) {
							try {
								filters.remove (item);
							}
							catch (__except0__) {
								if (isinstance (__except0__, Exception)) {
									// pass;
								}
								else {
									throw __except0__;
								}
							}
							filters.insert (0, item);
						}
						else if (!__in__ (item, filters)) {
							filters.append (item);
						}
						_filters_mutated ();
					};
					var resetwarnings = function () {
						var filters = list ([]);
						_filters_mutated ();
					};
					var __warningregistry__ = dict ({});
					var _checkCatMatch = function (msgCat, filtCat) {
						return msgCat.__name__ == filtCat.__name__;
					};
					var warn_explicit = function (message, category, filename, lineno, module, registry, module_globals) {
						if (typeof module == 'undefined' || (module != null && module .hasOwnProperty ("__kwargtrans__"))) {;
							var module = null;
						};
						if (typeof registry == 'undefined' || (registry != null && registry .hasOwnProperty ("__kwargtrans__"))) {;
							var registry = null;
						};
						if (typeof module_globals == 'undefined' || (module_globals != null && module_globals .hasOwnProperty ("__kwargtrans__"))) {;
							var module_globals = null;
						};
						var lineno = int (lineno);
						if (module === null) {
							var module = filename || '<unknown>';
							if (module.__getslice__ (-(3), null, 1).lower () == '.py') {
								var module = module.__getslice__ (0, -(3), 1);
							}
						}
						if (registry === null) {
							var registry = __warningregistry__;
						}
						try {
							var currVersion = registry ['version'];
						}
						catch (__except0__) {
							if (isinstance (__except0__, KeyError)) {
								var currVersion = 0;
							}
							else {
								throw __except0__;
							}
						}
						if (currVersion != _filters_version) {
							registry.py_clear ();
							registry ['version'] = _filters_version;
						}
						if (isinstance (message, Warning)) {
							var text = str (message);
							var category = message.__class__;
						}
						else {
							var text = message;
							var message = category (message);
						}
						var key = tuple ([text, category, lineno]);
						if (__in__ (key, registry)) {
							return ;
						}
						var __break0__ = false;
						for (var item of filters) {
							var __left0__ = item;
							var action = __left0__ [0];
							var msg = __left0__ [1];
							var cat = __left0__ [2];
							var mod = __left0__ [3];
							var ln = __left0__ [4];
							if ((msg === null || msg.match (text)) && _checkCatMatch (category, cat) && (mod === null || mod.match (module)) && (ln == 0 || lineno == ln)) {
								__break0__ = true;
								break;
							}
						}
						if (!__break0__) {
							var action = defaultaction;
						}
						if (action == Actions.ignore) {
							registry [key] = 1;
							return ;
						}
						if (action == Actions.error) {
							var __except0__ = message;
							__except0__.__cause__ = null;
							throw __except0__;
						}
						if (action == Actions.once) {
							registry [key] = 1;
							var oncekey = tuple ([text, category]);
							if (__in__ (oncekey, onceregistry)) {
								return ;
							}
							onceregistry [oncekey] = 1;
						}
						else if (action == Actions.always) {
							// pass;
						}
						else if (action == Actions.module) {
							registry [key] = 1;
							var altkey = tuple ([text, category, 0]);
							if (__in__ (altkey, registry)) {
								return ;
							}
							registry [altkey] = 1;
						}
						else if (action == Actions.defaultact) {
							registry [key] = 1;
						}
						else {
							var __except0__ = RuntimeError ('Unrecognized action ({}) in warnings.filters:\n {}'.format (action, item));
							__except0__.__cause__ = null;
							throw __except0__;
						}
						var msg = WarningMessage (message, category.__name__, filename, lineno);
						_showwarnmsg (msg);
					};
					var WarningMessage = __class__ ('WarningMessage', [object], {
						__module__: __name__,
						get __init__ () {return __get__ (this, function (self, message, category, filename, lineno, file, line) {
							if (typeof file == 'undefined' || (file != null && file .hasOwnProperty ("__kwargtrans__"))) {;
								var file = null;
							};
							if (typeof line == 'undefined' || (line != null && line .hasOwnProperty ("__kwargtrans__"))) {;
								var line = null;
							};
							self.message = message;
							self.category = category;
							self.filename = filename;
							self.lineno = lineno;
							self.file = file;
							self.line = line;
							self._category_name = (category ? category.__name__ : null);
						});},
						get __str__ () {return __get__ (this, function (self) {
							return '{{message : {}, category : {}, filename : {}, lineno : {}, line : {} }}'.format (self.message, self._category_name, self.filename, self.lineno, self.line);
						});}
					});
					var catch_warnings = __class__ ('catch_warnings', [object], {
						__module__: __name__,
						get __init__ () {return __get__ (this, function (self) {
							var record = false;
							var module = null;
							self._record = record;
							self._entered = false;
							var __except0__ = NotImplementedError ('with/as not well supported in transcrypt');
							__except0__.__cause__ = null;
							throw __except0__;
						});}
					});
					var setWarningOptions = function (opts) {
						_processoptions (opts);
					};
					var _OptionError = __class__ ('_OptionError', [Exception], {
						__module__: __name__,
					});
					var _processoptions = function (args) {
						for (var arg of args) {
							try {
								_setoption (arg);
							}
							catch (__except0__) {
								if (isinstance (__except0__, _OptionError)) {
									var msg = __except0__;
									console.log ('WARNING: Invalid -W option ignored: {}'.format (msg));
								}
								else {
									throw __except0__;
								}
							}
						}
					};
					var _setoption = function (arg) {
						var parts = arg.py_split (':');
						if (len (parts) > 5) {
							var __except0__ = _OptionError ('too many fields (max 5): {}'.format (arg));
							__except0__.__cause__ = null;
							throw __except0__;
						}
						while (len (parts) < 5) {
							parts.append ('');
						}
						var __left0__ = (function () {
							var __accu0__ = [];
							for (var s of parts) {
								__accu0__.append (s.strip ());
							}
							return __accu0__;
						}) ();
						var action = __left0__ [0];
						var message = __left0__ [1];
						var category = __left0__ [2];
						var module = __left0__ [3];
						var lineno = __left0__ [4];
						var action = _getaction (action);
						var message = re.escape (message);
						var category = _getcategory (category);
						var module = re.escape (module);
						if (module) {
							var module = module + '$';
						}
						if (lineno) {
							try {
								var lineno = int (lineno);
								if (lineno < 0) {
									var __except0__ = ValueError;
									__except0__.__cause__ = null;
									throw __except0__;
								}
							}
							catch (__except0__) {
								if (isinstance (__except0__, tuple ([ValueError, OverflowError]))) {
									var __except1__ = _OptionError ('invalid lineno {}'.format (lineno));
									__except1__.__cause__ = null;
									throw __except1__;
								}
								else {
									throw __except0__;
								}
							}
						}
						else {
							var lineno = 0;
						}
						filterwarnings (action, message, category, module, lineno);
					};
					var _getaction = function (action) {
						if (!(action)) {
							return Actions.defaultact;
						}
						if (action == 'all') {
							return Action.always;
						}
						for (var a of ActionSet) {
							if (a.startswith (action)) {
								return a;
							}
						}
						var __except0__ = _OptionError ('invalid action: {}'.format (action));
						__except0__.__cause__ = null;
						throw __except0__;
					};
					var _getcategory = function (category) {
						if (!(category)) {
							return Warning;
						}
						if (__in__ (category, CategoryMap.py_keys ())) {
							try {
								var cat = CategoryMap [category];
							}
							catch (__except0__) {
								if (isinstance (__except0__, NameError)) {
									var __except1__ = _OptionError ('unknown warning category: {}'.format (category));
									__except1__.__cause__ = null;
									throw __except1__;
								}
								else {
									throw __except0__;
								}
							}
						}
						else {
							var __except0__ = Exception ('Unable to import category: {}, use `addWarningCategory`'.format (category));
							__except0__.__cause__ = null;
							throw __except0__;
						}
						return cat;
					};
					if (!(_warnings_defaults)) {
						var silence = list ([DeprecationWarning]);
						for (var cls of silence) {
							simplefilter (Actions.ignore, __kwargtrans__ ({category: cls}));
						}
					}
					__pragma__ ('<use>' +
						're' +
					'</use>')
					__pragma__ ('<all>')
						__all__.ActionSet = ActionSet;
						__all__.Actions = Actions;
						__all__.CategoryMap = CategoryMap;
						__all__.WarningMessage = WarningMessage;
						__all__._OptionError = _OptionError;
						__all__.__name__ = __name__;
						__all__.__warningregistry__ = __warningregistry__;
						__all__._add_filter = _add_filter;
						__all__._checkCatMatch = _checkCatMatch;
						__all__._filters_mutated = _filters_mutated;
						__all__._filters_version = _filters_version;
						__all__._formatwarning = _formatwarning;
						__all__._formatwarnmsg = _formatwarnmsg;
						__all__._formatwarnmsg_impl = _formatwarnmsg_impl;
						__all__._getaction = _getaction;
						__all__._getcategory = _getcategory;
						__all__._processoptions = _processoptions;
						__all__._setoption = _setoption;
						__all__._showwarning = _showwarning;
						__all__._showwarnmsg = _showwarnmsg;
						__all__._showwarnmsg_impl = _showwarnmsg_impl;
						__all__._warnings_defaults = _warnings_defaults;
						__all__.addWarningCategory = addWarningCategory;
						__all__.catch_warnings = catch_warnings;
						__all__.cls = cls;
						__all__.defaultaction = defaultaction;
						__all__.filters = filters;
						__all__.filterwarnings = filterwarnings;
						__all__.formatwarning = formatwarning;
						__all__.onceregistry = onceregistry;
						__all__.resetwarnings = resetwarnings;
						__all__.setShowWarning = setShowWarning;
						__all__.setWarningOptions = setWarningOptions;
						__all__.showwarning = showwarning;
						__all__.silence = silence;
						__all__.simplefilter = simplefilter;
						__all__.warn_explicit = warn_explicit;
					__pragma__ ('</all>')
				}
			}
		}
	);
