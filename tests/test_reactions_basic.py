from __future__ import print_function, division, unicode_literals

from nose.tools import with_setup

from CAOS.dispatch import react, register_reaction_mechanism, \
    ReactionDispatcher
from CAOS.util import raises
from CAOS.exceptions.reaction_errors import FailedReactionError


def requirement1(r, c):
    return True


def requirement2(r, c):
    return False


class TestGeneratePotentialMechanisms(object):

    def teardown(self):
        for key in ['a', 'b', 'c']:
            if key in ReactionDispatcher._mechanism_namespace:
                del ReactionDispatcher._mechanism_namespace[key]

    # Test some stupidly simple cases without any real requirements
    def test_find_options_all_valid(self):

        @register_reaction_mechanism('a', {'requirement1': requirement1})
        def a(r, c):
            return ["Hello, world!"]

        @register_reaction_mechanism('b', {'requirement2': requirement1})
        def b(r, c):
            return ["Hello, world!"]

        @register_reaction_mechanism('c', {})
        def c(r, c_):
            return ["Hello, world!"]

        potential_mechanisms = ReactionDispatcher._generate_likely_reactions(
            None, None
        )
        assert all(function in potential_mechanisms for function in [a, b, c])

    def test_find_options_some_valid(self):

        @register_reaction_mechanism('a', {'requirement1': requirement1})
        def a(r, c):
            return ["Hello, world!"]

        @register_reaction_mechanism('b', {'requirement2': requirement2})
        def b(r, c):
            return ["Hello, world!"]

        @register_reaction_mechanism('c', {})
        def c(r, c_):
            return ["Hello, world!"]

        potential_mechanisms = ReactionDispatcher._generate_likely_reactions(
            None, None
        )
        assert a in potential_mechanisms
        assert c in potential_mechanisms
        assert b not in potential_mechanisms

    def test_find_options_none_valid(self):

        @register_reaction_mechanism('a', {'requirement1': requirement2})
        def a(r, c):
            return ["Hello, world!"]

        @register_reaction_mechanism('b', {'requirement2': requirement2})
        def b(r, c):
            return ["Hello, world!"]

        @register_reaction_mechanism('c', {'requirement3': requirement2})
        def c(r, c_):
            return ["Hello, world!"]

        potential_mechanisms = ReactionDispatcher._generate_likely_reactions(
            None, None
        )

        assert not any(function in potential_mechanisms for function in [a, b, c])


class TestPerformReactions(object):

    def teardown(self):
        for key in ['a', 'b', 'c']:
            if key in ReactionDispatcher._mechanism_namespace:
                del ReactionDispatcher._mechanism_namespace[key]

    def test_single_option(self):
        @register_reaction_mechanism('a', {})
        def a(r, c):
            return ["Hello, world!"]

        assert react(None, None) == ["Hello, world!"]

    def test_multiple_options(self):
        @register_reaction_mechanism('a', {})
        def a(r, c):
            return ["a"]

        @register_reaction_mechanism('b', {})
        def b(r, c):
            return ["b"]

        # The order is not guaranteed, but it should equal one of them.
        # This will be fixed once ordering is worked out.
        assert react(None, None) in (["a"], ["b"])

    def test_multiple_options_some_invalid(self):
        @register_reaction_mechanism('a', {})
        def a(r, c):
            return ["a"]

        @register_reaction_mechanism('b', {})
        def b(r, c):
            return ["b"]

        @register_reaction_mechanism('c', {'r2': requirement2})
        def c(r, c_):
            return ["c"]
            
        assert react(None, None) in (["a"], ["b"])

    def test_no_options(self):
        function = react
        args = [None, None]
        exception_type = FailedReactionError
        assert raises(exception_type, function, args)
