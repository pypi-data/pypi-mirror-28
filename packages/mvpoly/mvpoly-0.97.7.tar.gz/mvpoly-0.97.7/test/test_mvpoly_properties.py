# -*- coding: utf-8 -*-

# Property-tests courtesy of D. R. MacIver's Hypothesis
# http://hypothesis.works/

from mvpoly.cube import MVPolyCube
from mvpoly.dict import MVPolyDict

import numpy as np
import unittest
import warnings

warnings.simplefilter(action='ignore', category=FutureWarning)

from hypothesis import given, settings, strategies as st
from hypothesis.extra.numpy import arrays
from complex_numbers import complex_numbers

settings.register_profile(
    'ci',
    settings(
        deadline=None
    )
)
settings.load_profile('ci')

# Test classes specialised by underlying data structure and
# data type.  We want to use as little as possible of the
# internal machinery of the object, instead get to the
# underlying data representation and then make assertions on
# that.  The split on data-type is since in the integer case
# we obtain (and so can assert) exact results.

eps = 1e-17

class PropertyTest(unittest.TestCase):

    def assertPolyEq(self, p1, p2, msg, **kwarg):
        raise NotImplementedError()

    def assertPolyZero(self, p, msg, **kwargs):
        raise NotImplementedError()


class PropertyTestIntCube(PropertyTest):

    def assertPolyEq(self, p1, p2, msg, **kwarg):
        self.assertPolyZero(p1 - p2, msg)

    def assertPolyZero(self, p, msg, **kwarg):
        self._assertArrayZero(p.coef, msg)

    def _assertArrayZero(self, a, msg):
        self.assertTrue(np.all(a == 0), msg)


class PropertyTestFloatCube(PropertyTest):

    def assertPolyEq(self, p1, p2, msg, eps=eps):
        dp = p1 - p2
        shp = dp.coef.shape
        z = MVPolyCube(np.zeros(shp, dtype=dp.dtype), dtype=dp.dtype)
        a1 = (p1 + z).coef
        a2 = (p2 + z).coef
        self.assertTrue(np.all(np.isclose(a1, a2, rtol=eps)))

    def assertPolyZero(self, p, msg, eps=eps):
        self.assertPolyEq(p, MVPolyCube.zero(dtype=p.dtype), msg, eps=eps)


class PropertyTestIntDict(PropertyTest):

    def assertPolyEq(self, p1, p2, msg, **kwarg):
        self.assertTrue(p1.coef == p2.coef, msg)

    def assertPolyZero(self, p, msg, eps=eps):
        self.assertPolyEq(p, MVPolyDict.zero(dtype=p.dtype), msg)


class PropertyTestFloatDict(PropertyTest):

    def assertPolyEq(self, p1, p2, msg, eps=eps):
        for idx, _ in (p1 - p2).nonzero:
            p1i = p1[idx]
            p2i = p2[idx]
            pmax = max(abs(p1i), abs(p2i))
            self.assertTrue(abs(p1i - p2i) <= pmax * eps)

    def assertPolyZero(self, p, msg, eps=eps):
        self.assertPolyEq(p, MVPolyDict.zero(dtype=p.dtype), msg, eps=eps)


# the parameterised tests

def suite(poly, mvpoly_class, test_class):

    class RingAxioms(test_class):

        @given(poly, poly, poly)
        def test_addition_associative(self, p, q, r):
            self.assertPolyEq(
                (p + q) + r, p + (q + r),
                'addition associative'
            )

        @given(poly)
        def test_additive_identity(self, p):
            z = mvpoly_class.zero(dtype=p.dtype)
            self.assertPolyEq(
            z + p, p,
                'additive left identity'
            )
            self.assertPolyEq(
                p + z, p,
                'additive right identity'
            )

        @given(poly)
        def test_additive_inverse(self, p):
            self.assertPolyZero(
                p - p,
                'additive inverse'
            )

        @given(poly, poly)
        def test_addition_commutative(self, p, q):
            self.assertPolyEq(
                p + q, q + p,
                'addition commutative'
            )

        # need quite a large eps here; to investigate

        @given(poly, poly, poly)
        def test_multiplication_associative(self, p, q, r):
            self.assertPolyEq(
                (p * q) * r, p * (q * r),
                'multiplication associative',
                eps=1e-12
            )

        @given(poly)
        def test_mutiplicative_identity(self, p):
            one = mvpoly_class.one(dtype=p.dtype)
            self.assertPolyEq(
            one * p, p,
                'multiplicative left identity'
            )
            self.assertPolyEq(
                p * one, p,
                'multiplicative right identity'
            )

        @given(poly, poly)
        def test_multiplication_commutative(self, p, q):
            self.assertPolyEq(
                p * q, q * p,
                'multiplication_commutative'
            )

        @given(poly, poly, poly)
        def test_distributive(self, p, q, r):
            self.assertPolyEq(
                p * (q + r), p * q + p * r,
                'left distributative',
                eps=1e-16
            )
            self.assertPolyEq(
                (p + q) * r, p * r + q * r,
                'right distributative',
                eps=1e-15
            )

    return RingAxioms


# cube test-suites

def poly_strategy_cube(dtype, element_strategy):
    return st.builds(
        MVPolyCube,
        arrays(
            dtype,
            (2, 2),
            elements = element_strategy
        ),
        dtype = st.just(dtype)
    )

def suite_cube(dtype, element_strategy, property_test):
    poly = poly_strategy_cube(dtype, element_strategy)
    return suite(poly, MVPolyCube, property_test)

def suite_int_cube(dtype, element_strategy):
    return suite_cube(dtype, element_strategy, PropertyTestIntCube)

def suite_float_cube(dtype, element_strategy):
    return suite_cube(dtype, element_strategy, PropertyTestFloatCube)


class RingAxiomsIntCube(suite_int_cube(np.int, st.integers(-1000, 1000))):
    pass

class RingAxiomsFloatCube(suite_float_cube(np.float, st.floats(-1000, 1000))):
    pass

class RingAxiomsComplexCube(suite_float_cube(np.complex, complex_numbers(-1000, 1000))):
    pass


# dict test-suites

def poly_strategy_dict(dtype, element_strategy):
    return st.builds(
        MVPolyDict.init_from_nonzero_tuples,
        st.lists(
            max_size = 10,
            elements = st.tuples(
                st.tuples(
                    st.integers(0, 20),
                    st.integers(0, 20),
                    st.integers(0, 20)
                ),
                element_strategy
            )
        ),
        dtype = st.just(dtype)
    )

def suite_dict(dtype, element_strategy, property_test):
    poly = poly_strategy_dict(dtype, element_strategy)
    return suite(poly, MVPolyDict, property_test)

def suite_int_dict(dtype, element_strategy):
    return suite_dict(dtype, element_strategy, PropertyTestIntDict)

def suite_float_dict(dtype, element_strategy):
    return suite_dict(dtype, element_strategy, PropertyTestFloatDict)


class RingAxiomsIntDict(suite_int_dict(np.int, st.integers(-1000, 1000))):
    pass

class RingAxiomsFloatDict(suite_float_dict(np.float, st.floats(-1000, 1000))):
    pass

class RingAxiomsComplexDict(suite_float_dict(np.complex, complex_numbers(-1000, 1000))):
    pass
