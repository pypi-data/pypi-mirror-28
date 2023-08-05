	__nest__ (
		__all__,
		'basics', {
			__all__: {
				__inited__: false,
				__init__: function (__all__) {
					var __name__ = 'basics';
					if (__envir__.executor_name == __envir__.transpiler_name) {
						var num =  __init__ (__world__.numscrypt);
					}
					var run = function (autoTester) {
						var z = num.zeros (tuple ([4, 3]), 'int32');
						autoTester.check ('Zeros', z.tolist (), '<br>');
						var o = num.ones (tuple ([4, 5]));
						autoTester.check ('Ones', o.astype ('int32').tolist ());
						var i = num.identity (3, 'int32');
						autoTester.check ('Identity', i.tolist (), '<br>');
						var a = num.array (list ([list ([1, 1, 2, 3]), list ([4, 5, 6, 7]), list ([8, 9, 10, 12])]));
						autoTester.check ('Matrix a', a.tolist (), '<br>');
						autoTester.check ('Transpose of a', a.transpose ().tolist (), '<br>');
						var b = num.array (list ([list ([2, 2, 4, 6]), list ([8, 10, 12, 14]), list ([16, 18, 20, 24])]));
						var bp = b.transpose ();
						autoTester.check ('Matrix b', b.tolist (), '<br>');
						autoTester.check ('Permutation of b', bp.tolist (), '<br>');
						var c = num.array (list ([list ([1, 2, 3, 4]), list ([5, 6, 7, 8]), list ([9, 10, 11, 12])]), 'int32');
						autoTester.check ('Shape c', tuple (c.shape), '<br>');
						autoTester.check ('Matrix c', c.tolist (), '<br>');
						var ct = c.transpose ();
						autoTester.check ('Shape ct', tuple (ct.shape), '<br>');
						autoTester.check ('Transpose of c', ct.tolist (), '<br>');
						var __left0__ = num.hsplit (c, 2);
						var cs0 = __left0__ [0];
						var cs1 = __left0__ [1];
						autoTester.check ('Matrix cs0', cs0.tolist (), '<br>');
						autoTester.check ('Matrix cs1', cs1.tolist (), '<br>');
						var ci = num.hstack (tuple ([cs1, cs0]));
						autoTester.check ('Matrix ci', ci.tolist (), '<br>');
						var __left0__ = num.hsplit (ct, 3);
						var cts0 = __left0__ [0];
						var cts1 = __left0__ [1];
						var cts2 = __left0__ [2];
						autoTester.check ('Matrix cts0', cts0.tolist (), '<br>');
						autoTester.check ('Matrix cts1', cts1.tolist (), '<br>');
						autoTester.check ('Matrix cts2', cts2.tolist (), '<br>');
						var cti = num.hstack (tuple ([cts2, cts1, cts0]));
						autoTester.check ('Matrix ci', cti.tolist (), '<br>');
						var d = num.array (list ([list ([13, 14]), list ([15, 16]), list ([17, 18]), list ([19, 20])]), 'int32');
						autoTester.check ('Matrix d', d.tolist (), '<br>');
						var dt = d.transpose ();
						autoTester.check ('Permutation of d', dt.tolist (), '<br>');
						var __left0__ = num.vsplit (d, 4);
						var ds0 = __left0__ [0];
						var ds1 = __left0__ [1];
						var ds2 = __left0__ [2];
						var ds3 = __left0__ [3];
						autoTester.check ('Matrix ds0', ds0.tolist (), '<br>');
						autoTester.check ('Matrix ds1', ds1.tolist (), '<br>');
						autoTester.check ('Matrix ds2', ds2.tolist (), '<br>');
						autoTester.check ('Matrix ds3', ds3.tolist (), '<br>');
						var di = num.vstack (tuple ([ds3, ds2, ds1, ds0]));
						autoTester.check ('Matrix di', di.tolist (), '<br>');
						var __left0__ = num.vsplit (dt, 2);
						var dts0 = __left0__ [0];
						var dts1 = __left0__ [1];
						autoTester.check ('Matrix dts0', dts0.tolist (), '<br>');
						autoTester.check ('Matrix dts1', dts1.tolist (), '<br>');
						var dti = num.vstack (tuple ([dts1, dts0]));
						autoTester.check ('Matrix dti', dti.tolist (), '<br>');
						var v0 = num.array (range (10));
						var v1 = num.array (tuple ([1, 2, 3, 1, 2, 3, 1, 2, 3, 1]));
						a.__setitem__ ([1, 0], 177);
						var el = b.__getitem__ ([1, 2]);
						var bsl0 = b.__getitem__ ([1, tuple ([1, 3, 1])]);
						var bsl1 = b.__getitem__ ([tuple ([1, 2, 1]), tuple ([1, 3, 1])]);
						var bsl2 = b.__getitem__ ([tuple ([1, 2, 1]), 1]);
						var bsl3 = b.__getitem__ ([1, tuple ([1, 3, 1])]);
						var bsl4 = b.__getitem__ ([tuple ([0, null, 1]), 1]);
						var bsl5 = b.__getitem__ ([1, tuple ([1, 3, 1])]);
						var bsl6 = b.__getitem__ ([1, tuple ([1, 3, 1])]);
						var bsl7 = b.__getitem__ ([1, tuple ([2, 3, 1])]);
						var bpsl0 = bp.__getitem__ ([1, tuple ([1, 3, 1])]);
						var bpsl1 = bp.__getitem__ ([tuple ([1, 2, 1]), tuple ([1, 3, 1])]);
						var bpsl2 = bp.__getitem__ ([1, tuple ([0, null, 1])]);
						var bpsl3 = bp.__getitem__ ([1, tuple ([1, 3, 1])]);
						var bpsl4 = bp.__getitem__ ([tuple ([0, null, 1]), 1]);
						var bpsl5 = bp.__getitem__ ([3, tuple ([1, 3, 1])]);
						var bpsl6 = bp.__getitem__ ([tuple ([2, 4, 1]), tuple ([1, 3, 1])]);
						var bpsl7 = bp.__getitem__ ([tuple ([2, 4, 1]), tuple ([2, 3, 1])]);
						var sum = __add__ (a, b);
						var dif = __sub__ (a, b);
						var prod = __mul__ (a, b);
						var quot = __truediv__ (a, b);
						var dot = __matmul__ (c, d);
						var vsum = __add__ (v0, v1);
						var vel = __getitem__ (vsum, 6);
						__setitem__ (vsum, 6, 70);
						var mul_a3 = __mul__ (a, 3);
						var mul_3a = __mul__ (3, a);
						var div_a3 = __truediv__ (a, 3.1234567);
						var div_3a = __truediv__ (3.1234567, a);
						var add_a3 = __add__ (a, 3);
						var add_3a = __add__ (3, a);
						var sub_a3 = __sub__ (a, 3);
						var sub_3a = __sub__ (3, a);
						var neg_a = __neg__ (a);
						autoTester.check ('El a [1, 2, 3] alt', a.tolist (), '<br>');
						autoTester.check ('El b [1, 2, 3]', el, '<br>');
						autoTester.check ('Sl b0', bsl0.tolist (), '<br>');
						autoTester.check ('Sl b1', bsl1.tolist (), '<br>');
						autoTester.check ('Sl b2', bsl2.tolist (), '<br>');
						autoTester.check ('Sl b3', bsl3.tolist (), '<br>');
						autoTester.check ('Sl b4', bsl4.tolist (), '<br>');
						autoTester.check ('Sl b5', bsl5.tolist (), '<br>');
						autoTester.check ('Sl b6', bsl6.tolist (), '<br>');
						autoTester.check ('Sl b7', bsl7.tolist (), '<br>');
						autoTester.check ('Sl bp0', bpsl0.tolist (), '<br>');
						autoTester.check ('Sl bp1', bpsl1.tolist (), '<br>');
						autoTester.check ('Sl bp2', bpsl2.tolist (), '<br>');
						autoTester.check ('Sl bp3', bpsl3.tolist (), '<br>');
						autoTester.check ('Sl bp4', bpsl4.tolist (), '<br>');
						autoTester.check ('Sl bp5', bpsl5.tolist (), '<br>');
						autoTester.check ('Sl bp6', bpsl6.tolist (), '<br>');
						autoTester.check ('Sl bp7', bpsl7.tolist (), '<br>');
						autoTester.check ('Matrix sum', sum.tolist (), '<br>');
						autoTester.check ('Matrix difference', dif.tolist (), '<br>');
						autoTester.check ('Matrix product', prod.tolist (), '<br>');
						autoTester.check ('Matrix quotient', quot.tolist (), '<br>');
						autoTester.check ('Matrix dotproduct', dot.tolist (), '<br>');
						autoTester.check ('Vector', v0.tolist (), '<br>');
						autoTester.check ('Vector', v1.tolist (), '<br>');
						autoTester.check ('El sum old', vel, '<br>');
						autoTester.check ('Vector sum new', vsum.tolist (), '<br>');
						autoTester.check ('mul_a3', mul_a3.tolist (), '<br>');
						autoTester.check ('mul_3a', mul_3a.tolist (), '<br>');
						autoTester.check ('div_a3', num.round (div_a3, 2).tolist (), '<br>');
						autoTester.check ('div_3a', num.round (div_3a, 2).tolist (), '<br>');
						autoTester.check ('add_a3', add_a3.tolist (), '<br>');
						autoTester.check ('add_3a', add_3a.tolist (), '<br>');
						autoTester.check ('sub_a3', sub_a3.tolist (), '<br>');
						autoTester.check ('sub_3a', sub_3a.tolist (), '<br>');
						autoTester.check ('neg_a', neg_a.tolist (), '<br>');
						var comp_a = __call__ (num.array, num, list ([list ([__add__ (1, complex (0, 2.0)), __sub__ (2, complex (0, 1.0)), 3]), list ([4, __add__ (5, complex (0, 3.0)), 7])]), 'complex128');
						var comp_b = __call__ (num.array, num, list ([list ([6, __sub__ (8, complex (0, 1.0))]), list ([__add__ (9, complex (0, 3.0)), 10]), list ([11, __sub__ (12, complex (0, 6.0))])]), 'complex128');
						var comp_c = __matmul__ (comp_a, comp_b);
						autoTester.check ('comp_a', comp_a.tolist (), '<br>');
						autoTester.check ('comp_b', comp_b.tolist (), '<br>');
						autoTester.check ('comp_c', comp_c.tolist (), '<br>');
						var comp_a_square = comp_a.__getitem__ ([tuple ([0, null, 1]), tuple ([0, 2, 1])]);
						var comp_b_square = comp_b.__getitem__ ([tuple ([1, null, 1]), tuple ([0, null, 1])]);
						var comp_c_square = __mul__ (comp_a_square, comp_b_square);
						var comp_d_square = __truediv__ (comp_a_square, comp_b_square);
						var comp_e_square = __add__ (comp_a_square, comp_b_square);
						var comp_f_square = __sub__ (comp_a_square, comp_b_square);
						autoTester.check ('comp_a_square', comp_a_square.tolist (), '<br>');
						autoTester.check ('comp_b_square', comp_b_square.tolist (), '<br>');
						autoTester.check ('comp_c_square', comp_c_square.tolist (), '<br>');
						autoTester.check ('comp_d_square', num.round (comp_d_square, 2).tolist (), '<br>');
						autoTester.check ('comp_e_square', comp_e_square.tolist (), '<br>');
						autoTester.check ('comp_f_square', comp_f_square.tolist (), '<br>');
						var sliceable_a = __call__ (num.array, num, list ([list ([1, 2, 3, 4]), list ([5, 6, 7, 8]), list ([9, 10, 11, 12]), list ([13, 14, 15, 16])]));
						__call__ (autoTester.check, autoTester, 'sliceable_a', __call__ (sliceable_a.tolist, sliceable_a));
						var slice_a = sliceable_a.__getitem__ ([tuple ([1, null, 1]), tuple ([1, null, 1])]);
						__call__ (autoTester.check, autoTester, 'slice_a');
						var sliceable_at = __call__ (sliceable_a.transpose, sliceable_a);
						var slice_at = __getslice__ (sliceable_at, 1, null, 1);
					};
					__pragma__ ('<use>' +
						'numscrypt' +
					'</use>')
					__pragma__ ('<all>')
						__all__.__name__ = __name__;
						__all__.run = run;
					__pragma__ ('</all>')
				}
			}
		}
	);
