	(function () {
		var basics = {};
		var module_fft = {};
		var module_linalg = {};
		var org = {};
		var __name__ = '__main__';
		__nest__ (org, 'transcrypt.autotester', __init__ (__world__.org.transcrypt.autotester));
		__nest__ (basics, '', __init__ (__world__.basics));
		__nest__ (module_linalg, '', __init__ (__world__.module_linalg));
		__nest__ (module_fft, '', __init__ (__world__.module_fft));
		var autoTester = org.transcrypt.autotester.AutoTester ();
		autoTester.run (basics, 'basics');
		autoTester.run (module_linalg, 'module_linalg');
		autoTester.run (module_fft, 'module_fft');
		autoTester.done ();
		__pragma__ ('<use>' +
			'basics' +
			'module_fft' +
			'module_linalg' +
			'org.transcrypt.autotester' +
		'</use>')
		__pragma__ ('<all>')
			__all__.__name__ = __name__;
			__all__.autoTester = autoTester;
		__pragma__ ('</all>')
	}) ();
