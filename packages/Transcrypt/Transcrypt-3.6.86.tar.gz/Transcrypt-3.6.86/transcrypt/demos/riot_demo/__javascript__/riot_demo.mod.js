	(function () {
		var __name__ = '__main__';
		var RiotTag = __init__ (__world__.riot_tag).RiotTag;
		var P = __class__ ('P', [RiotTag], {
			__module__: __name__,
			debug: 1,
			lv: list ([dict ({'name': 'n0'})]),
			counter: 1,
			template: ' <div><h1>Riot Transcrypt Tag Instance {label}</h1>\n                         <div>INNER</div></div> ',
			get count_up () {return __get__ (this, function (self) {
				self.counter = self.counter + 1;
				self.pp ('counter:', self.counter, 'len lv:', len (self.lv), 'adding one lv');
				self.lv.append (dict ({'name': 'n' + self.counter}));
				return self.counter;
			});}
		});
		var Sample2 = __class__ ('Sample2', [P], {
			__module__: __name__,
			template: P.template.py_replace ('INNER', '\n    <div>\n    <h5 each="{lv}">name: {name} - counter: {count_up()}</h5>\n    </div>\n    '),
			style: 'sample2 h5 {color: green}',
			get __init__ () {return __get__ (this, function (self, tag, opts) {
				self.label = opts.label.capitalize ();
				RiotTag.__init__ (self, tag, opts);
				self.pp ('tag init', 'adding 2 lv');
				self.lv.extend (list ([dict ({'name': 'n1'}), dict ({'name': 'n2'})]));
			});},
			get py_update () {return __get__ (this, function (self) {
				self.pp ('update handler in the custom tag, calling super');
				RiotTag.py_update (self);
			});}
		});
		__pragma__ ('<use>' +
			'riot_tag' +
		'</use>')
		__pragma__ ('<all>')
			__all__.P = P;
			__all__.RiotTag = RiotTag;
			__all__.Sample2 = Sample2;
			__all__.__name__ = __name__;
		__pragma__ ('</all>')
	}) ();
