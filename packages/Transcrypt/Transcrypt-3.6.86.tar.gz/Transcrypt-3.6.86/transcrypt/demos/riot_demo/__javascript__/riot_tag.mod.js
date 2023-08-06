	__nest__ (
		__all__,
		'riot_tag', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'riot_tag';
					var __author__ = 'Gunther Klessinger, gk@axiros.com, Germany';
					var colors = __init__ (__world__.color).colors;
					var col_print = __init__ (__world__.color).cprint;
					var c = colors;
					var __left0__ = tuple ([c ['purple'], c ['orange'], c ['gray'], c ['red'], c ['black']]);
					var M = __left0__ [0];
					var I = __left0__ [1];
					var L = __left0__ [2];
					var R = __left0__ [3];
					var B = __left0__ [4];
					var lifecycle_ev = list (['before-mount', 'mount', 'update', 'unmount']);
					var cur_tag_col = 0;
					var RiotTag = __class__ ('RiotTag', [object], {
						__module__: __name__,
						debug: null,
						template: '<h1>it worx</h1>',
						style: '',
						node_name: 'unmounted',
						opts: null,
						get __init__ () {return __get__ (this, function (self, tag, opts) {
							self.opts = opts;
							self._setup_tag (tag);
							cur_tag_col = __mod__ (cur_tag_col + 1, len (colors));
							self.my_col = colors.py_items () [cur_tag_col] [1];
						});},
						get _setup_tag () {return __get__ (this, function (self, tag) {
							tag.py_obj = self;
							self.riot_tag = tag;
							var handlers = dict ({});
							for (var ev of lifecycle_ev) {
								var f = getattr (self, ev.py_replace ('-', '_'));
								if (f) {
									tag.on (ev, f);
								}
							}
						});},
						get pp () {return __get__ (this, function (self) {
							var msg = tuple ([].slice.apply (arguments).slice (1));
							col_print (L ('<', self.my_col (self.node_name, self.my_col), '/> '), M (' '.join ((function () {
								var __accu0__ = [];
								for (var s of msg) {
									__accu0__.append (s);
								}
								return __accu0__;
							}) ())));
						});},
						get _lifecycle_ev () {return __get__ (this, function (self, mode) {
							if (self.debug) {
								self.pp (mode + 'ing');
							}
						});},
						get py_update () {return __get__ (this, function (self) {
							self._lifecycle_ev ('update');
						});},
						get mount () {return __get__ (this, function (self) {
							self._lifecycle_ev ('mount');
						});},
						get unmount () {return __get__ (this, function (self) {
							self._lifecycle_ev ('unmount');
						});},
						get before_mount () {return __get__ (this, function (self) {
							self._lifecycle_ev ('before-mount');
							return self.bind_vars ();
						});},
						get bind_vars () {return __get__ (this, function (self) {
							var tag = self.riot_tag;
							self.node_name = tag.root.nodeName.lower ();
							self.debug && self.pp ('binding vars');
							var __left0__ = list ([]);
							tag._immutables = __left0__;
							var im = __left0__;
							var lc = lifecycle_ev;
							for (var k of dir (self)) {
								if (k [0] == '_' || __in__ (k, lifecycle_ev) || k == 'before_mount') {
									continue;
								}
								var v = getattr (self, k);
								
								                  typeof v === "function" || typeof v === "object" ?
								                  tag[k] = self[k] : tag._immutables.push(k)
							}
							
							        var i = tag._immutables, py = self
							        i.forEach(function(k, j, i) {
							            Object.defineProperty(tag, k, {
							                get: function()  { return self[k]},
							                set: function(v) { self[k] = v }
							            })
							        })
						});}
					});
					__pragma__ ('<use>' +
						'color' +
					'</use>')
					__pragma__ ('<all>')
						__all__.B = B;
						__all__.I = I;
						__all__.L = L;
						__all__.M = M;
						__all__.R = R;
						__all__.RiotTag = RiotTag;
						__all__.__author__ = __author__;
						__all__.__name__ = __name__;
						__all__.c = c;
						__all__.col_print = col_print;
						__all__.colors = colors;
						__all__.cur_tag_col = cur_tag_col;
						__all__.lifecycle_ev = lifecycle_ev;
					__pragma__ ('</all>')
				}
			}
		}
	);
