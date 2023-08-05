import sys; sys.path.append("../")

import unittest
import copy

from delimited.path import TuplePath
from delimited.path import DelimitedStrPath
from delimited.container import NestedDict
from delimited.container import DelimitedDict


class TestNestedContainer(unittest.TestCase):

    # __init__

    def test___init____no_params(self):
        a = NestedDict()
        self.assertEqual(a.data, {})

    def test___init____dict_param(self):
        a = NestedDict({("k",): "v"})
        self.assertEqual(a, {"k": "v"})

    def test___init____tuple_notation_dict_param(self):
        a = NestedDict({("k1", "k2", "k3"): "v"})
        self.assertEqual(a, {"k1": {"k2": {"k3": "v"}}})

    # __call__

    def test___call____no_params(self):
        a = NestedDict({("k1", "k2", "k3"): "v"})
        a()
        self.assertEqual(a, {})

    def test___call____dict_param(self):
        a = NestedDict()
        a({("k",): "v"})
        self.assertEqual(a, {"k": "v"})

    def test___call____tuple_notation_dict_param(self):
        a = NestedDict()
        a({("k1", "k2", "k3"): "v"})
        self.assertEqual(a, {"k1": {"k2": {"k3": "v"}}})

    # __bool__

    def test___bool____empty_dict__returns_False(self):
        self.assertFalse(bool(NestedDict()))

    def test___bool____non_empty_dict__returns_True(self):
        self.assertTrue(bool(NestedDict({("k1", "k2", "k3"): "v"})))

    # __repr__

    def test___repr__(self):
        a = NestedDict({("k",): "v"})
        self.assertEqual(repr(a), "NestedDict({'k': 'v'})")

    # __eq__

    def test___eq____returns_True(self):
        a1 = NestedDict({("k1", "k2", "k3"): "v"})
        a2 = NestedDict({("k1", "k2", "k3"): "v"})
        self.assertTrue(a1 == a2)

    def test___eq____same_class__returns_False(self):
        a1 = NestedDict({("foo", "bar"): "baz"})
        a2 = NestedDict({("bar", "baz"): "foo"})
        self.assertFalse(a1 == a2)

    def test___eq____different_class__returns_True(self):
        a1 = NestedDict({("foo", "bar"): "baz"})
        a2 = {"foo": {"bar": "baz"}}
        self.assertTrue(a1 == a2)

        a3 = NestedDict()
        a4 = {}
        self.assertTrue(a3 == a4)

    # __ne__

    def test___ne____returns_True(self):
        a1 = NestedDict({("foo", "bar"): "baz"})
        a2 = NestedDict({("bar", "baz"): "foo"})
        self.assertTrue(a1 != a2)

    def test___ne____returns_False(self):
        a1 = NestedDict({("k1", "k2", "k3"): "v"})
        a2 = NestedDict({("k1", "k2", "k3"): "v"})
        self.assertFalse(a1 != a2)

    # __hash__

    def test___hash__(self):
        a1 = hash(NestedDict({("k1", "k2", "k3"): "v"}))
        a2 = hash(NestedDict({("k1", "k2", "k3"): "v"}))
        self.assertTrue(a1 == a2)

    # __iter__

    def test___iter__(self):
        a = NestedDict({("a", "a", "a"): "v"})
        for k, v in a:
            self.assertEqual(k, "a")

    # __contains__

    def test___contains__(self):
        a = NestedDict({("k1", "k2", "k3"): "v"})
        self.assertTrue(("k1",) in a)

    # __getitem__

    def test___getitem__tuple_param__returns_value(self):
        a = NestedDict({("k1", "k2", "k3"): "v"})
        self.assertEqual(a[("k1",)], {"k2": {"k3": "v"}})

    def test___getitem__delimited_tuple_param__returns_value(self):
        a = NestedDict({("k1", "k2", "k3"): "v"})
        self.assertEqual(a[("k1", "k2", "k3")], "v")

    # __setitem__

    def test___setitem__string_param__sets_value(self):
        a = NestedDict({("k1", "k2", "k3"): "v"})
        a[("k1",)] = "foo"
        self.assertEqual(a.data, {"k1": "foo"})

    def test___setitem__delimited_string_param__sets_value(self):
        a = NestedDict({("k1", "k2", "k3"): "v"})
        a[("k1", "k2", "k3")] = "foo"
        self.assertEqual(a.data, {"k1": {"k2": {"k3": "foo"}}})

    # __delitem__

    def test___delitem__string_param__deletes_value(self):
        a = NestedDict({("k1", "k2", "k3"): "v"})
        del a[("k1",)]
        self.assertEqual(a.data, {})

    def test___delitem__delimited_string_param__deletes_value(self):
        a = NestedDict({("k1", "k2", "k3"): "v"})
        del a[("k1", "k2")]
        self.assertEqual(a.data, {"k1": {}})

    # __len__

    def test___len__(self):
        a = NestedDict({("foo",): "v", ("bar",): "v", ("baz",): "v"})
        self.assertEqual(len(a), 3)

    # __copy__

    def test___copy__(self):
        a1 = NestedDict({("k1", "k2", "k3"): "v"})
        a2 = copy.copy(a1)
        
        self.assertIsNot(a1, a2)
        self.assertEqual(a1, a2)
        a1.set(("k1", "k2"), "bar")
        self.assertEqual(a1, a2)

    # __deepcopy__

    def test___deepcopy__(self):
        a1 = NestedDict({("k1", "k2", "k3"): "v"})
        a2 = copy.deepcopy(a1)
        self.assertIsNot(a1, a2)
        self.assertEqual(a1, a2)
        a1.set(["k1", "k2"], "bar")
        self.assertNotEqual(a1, a2)

    # __items__

    def test___items___for_item__yields_tuple(self):
        a = NestedDict({("k",): "v"})
        for item in a.items():
            self.assertIsInstance(item, tuple)

    # __keys__

    def test___keys___yields_keys(self):
        a = NestedDict({("k",): "v"})
        for k in a.keys():
            self.assertEqual(k, "k")

    # __values__

    def test___values___yields_values(self):
        a = NestedDict({("k",): "v"})
        for v in a.values():
            self.assertEqual(v, "v")

    # ref

    def test_ref__no_param__returns_all_attributes(self):
        a = NestedDict({("k",): "v"})
        self.assertEqual(a.ref(), {"k": "v"})

    def test_ref__string_param__returns_value(self):
        a = NestedDict({("k",): "v"})
        self.assertEqual(a.ref("k"), "v")

    def test_ref__string_param__raises_KeyError(self):
        a = NestedDict()
        with self.assertRaises(KeyError):
            a.ref("k")

    def test_ref__string_param__raises_ValueError(self):
        a = NestedDict({("k1", "k2"): "v"})
        with self.assertRaises(TypeError):
            a.ref(("k1", "k2", "k3"))

    def test_ref__delimited_string_param__returns_value(self):
        a = NestedDict({("k1", "k2", "k3"): "v"})
        self.assertEqual(a.ref(("k1", "k2")), ({"k3": "v"}))

    def test_ref__True_create_param_key_missing__creates_missing_containers(self):
        a = NestedDict()
        a.ref("k", create=True)
        self.assertEqual(a, {"k": {}})

    # get

    def test_get__string_param__returns_value(self):
        a = NestedDict({"k": "v"})
        self.assertEqual(a.get("k"), "v")

    def test_get__string_param_missing_key__returns_default_value(self):
        a = NestedDict()
        self.assertEqual(a.get("k", "foo"), "foo")

    def test_get__string_param__raises_KeyError(self):
        a = NestedDict()
        with self.assertRaises(KeyError):
            a.get("k")

    def test_get__string_param__raises_ValueError(self):
        a = NestedDict({("k1", "k2"): "v"})
        with self.assertRaises(TypeError):
            a.get(["k1", "k2", "k3"])

    def test_get__delimited_string_param__returns_value(self):
        a = NestedDict({("k1", "k2", "k3"): "v"})
        self.assertEqual(a.get(("k1", "k2")), {"k3": "v"})

    # has

    def test_has__no_params__returns_True(self):
        self.assertTrue(NestedDict({"k": "v"}).has())

    def test_has__no_params__returns_False(self):
        self.assertFalse(NestedDict().has())

    def test_has__tuple_param__returns_True(self):
        a = NestedDict({("k1", "k2", "k3"): "v"})
        self.assertTrue(a.has(("k1",)))

    def test_has__tuple_param__returns_False(self):
        a = NestedDict({("k1", "k2", "k3"): "v"})
        self.assertFalse(a.has(("foo",)))

    def test_has__delimited_tuple_param__returns_True(self):
        a = NestedDict({("k1", "k2", "k3"): "v"})
        self.assertTrue(a.has(("k1", "k2", "k3")))

    def test_has__delimited_tuple_param__returns_False(self):
        a = NestedDict({("k1", "k2", "k3"): "v"})
        self.assertFalse(a.has(("k1", "k2", "foo")))

    # copy

    def test_copy(self):
        a1 = NestedDict({("k1", "k2", "k3"): "v"})
        a2 = a1.copy()
        self.assertEqual(a1, a2)
        a1["k1"] = "foo"
        self.assertNotEqual(a1, a2)

    # clone

    def test_clone(self):
        a1 = NestedDict({("k1", "k2", "k3"): "v"})
        a2 = a1.clone()
        self.assertEqual(a1, a2)
        a1["k1"] = "foo"
        self.assertEqual(a1, a2)

    # set

    def test_set__string_key_param(self):
        a = NestedDict()
        a.set("k", "v")
        self.assertEqual(a, {"k": "v"})

    def test_set__delimited_string_key_param(self):
        a = NestedDict()
        a.set(("k1", "k2", "k3"), "v")
        self.assertEqual(a, {"k1": {"k2": {"k3": "v"}}})

    def test_set__raises_TypeError(self):
        a = NestedDict({("k1", "k2"): "v"})
        with self.assertRaises(TypeError):
            a.set(("k1", "k2", "k3"), "v", create=False)

    # push

    def test_push__string_key_param(self):
        a = NestedDict({"k": []})
        a.push(("k",), "v")
        self.assertEqual(a, {"k": ["v"]})

    def test_push__string_key_param__convert_existing_value(self):
        a = NestedDict({"k": "v"})
        a.push(("k",), "v")
        self.assertEqual(a, {"k": ["v", "v"]})

    def test_push__delimited_string_key_param(self):
        a = NestedDict({("k1", "k2", "k3"): []})
        a.push(("k1", "k2", "k3"), "v")
        self.assertEqual(a, {"k1": {"k2": {"k3": ["v"]}}})

    def test_push__True_create_param__creates_list(self):
        a = NestedDict()
        a.push(("k",), "v")
        self.assertEqual(a, {"k": ["v"]})

    def test_push__create_False__raises_KeyError(self):
        a = NestedDict()
        with self.assertRaises(KeyError):
            a.push(("k",), "v", create=False)

    def test_psuh__create_False__raises_TypeError(self):
        a = NestedDict({"k": "v"})
        with self.assertRaises(AttributeError):
            a.push(("k",), "v", create=False)

    # pull

    def test_pull__string_key_param(self):
        a = NestedDict({("k",): ["v"]})
        a.pull(("k",), "v")
        self.assertEqual(a, {"k": []})

    def test_pull__cleanup_True__removes_empty_containers(self):
        a = NestedDict({("k",): ["v"]})
        a.pull(("k",), "v", cleanup=True)
        self.assertEqual(a, {})

    def test_pull__delimited_string_key_param(self):
        a = NestedDict({("k1", "k2", "k3"): ["v"]})
        a.pull(("k1", "k2", "k3"), "v")
        self.assertEqual(a, {"k1": {"k2": {"k3": []}}})

    def test_pull__string_key_param__raises_KeyError(self):
        a = NestedDict()
        with self.assertRaises(KeyError):
            a.pull(("k",), "v")

    def test_pull__string_key_param__raises_ValueError(self):
        a = NestedDict({"k": []})
        with self.assertRaises(ValueError):
            a.pull(("k",), "v")

    def test_pull__string_key_param__raises_TypeError(self):
        a = NestedDict({("k",): "v"})
        with self.assertRaises(AttributeError):
            a.pull(("k",), "v")

    # unset

    def test_unset__string_key_param(self):
        a = NestedDict({("k",): "v"})
        a.unset(("k",))
        self.assertEqual(a, {})

    def test_unset__cleanup_True__removes_empty_containers(self):
        a = NestedDict({("k1", "k2", "k3"): "v"})
        a.unset(("k1", "k2", "k3"), cleanup=True)
        self.assertEqual(a, {})

    def test_unset__string_key_param__raises_KeyError(self):
        a = NestedDict({("k",): "v"})
        with self.assertRaises(KeyError):
            a.unset(("foo",))

    # _merge

    def test__merge__dict_params(self):
        a1 = {("k1",): "v"}
        a2 = {("k2",): "v"}
        a = NestedDict._merge(a1, a2)
        self.assertEqual(type(a), dict)
        self.assertEqual(a, {
            ("k1",): "v",
            ("k2",): "v"
        })

    def test__merge__nested_dict_params(self):
        a1 = {("foo",): "v", ("bar",): {("baz",): "v"}}
        a2 = {("bar",): {("qux",): "v"}}
        a = NestedDict._merge(a1, a2)
        self.assertEqual(type(a), dict)
        self.assertEqual(a, {
            ("foo",): "v",
            ("bar",): {
                ("baz",): "v",
                ("qux",): "v"
            }
        })

    def test__merge__NestedDict_params(self):
        a1 = NestedDict({("k1",): "v"})
        a2 = NestedDict({("k2",): "v"})
        a = NestedDict._merge(a1, a2)
        self.assertEqual(type(a), NestedDict)
        self.assertEqual(a, NestedDict({
            ("k1",): "v",
            ("k2",): "v"
        }))

    # merge

    def test_merge__dict_param(self):
        a = NestedDict({("k1",): "v"})

        b = a.merge({("k2",): "v"})
        self.assertEqual(b, {
            "k1": "v",
            "k2": "v"
        })

    def test_merge__NestedDict_param(self):
        a = NestedDict({("k1",): "v"})
        b = a.merge(NestedDict({("k2",): "v"}))
        self.assertEqual(b, {
            "k1": "v",
            "k2": "v"
        })

    # update

    def test_update__dict_param(self):
        a = NestedDict({("k1",): "v"})
        a.update({("k2",): "v"})
        self.assertEqual(a, {
            "k1": "v",
            "k2": "v"
        })

    def test_update__NestedDict_param(self):
        a = NestedDict({("k1",): "v"})
        a.update(NestedDict({("k2",): "v"}))
        self.assertEqual(a, {
            "k1": "v",
            "k2": "v"
        })

    # _collapse

    def test__collapse(self):
        data = {("k1",): {("k2",): {("k3",): "v"}}}
        b = NestedDict()
        b.data = {("k1", "k2", "k3"): "v"}
        self.assertEqual(NestedDict._collapse(data), b)

    def test__collapse__empty_dict(self):
        data = {("k1",): {("k2",): {("k3",): {}}}}
        b = NestedDict()
        b.data = {("k1", "k2", "k3"): {}}
        self.assertEqual(NestedDict._collapse(data), b)

    # collapse

    def test_collapse(self):
        a = NestedDict({("k1",): {("k2",): {("k3",): "v"}}})
        b = a.collapse()
        self.assertEqual(b, {("k1", "k2", "k3"): "v"})

    def test_collapse__function_param(self):
        a = NestedDict({("k1", "k2", "$foo", "k3", "k4"): "v"})

        def detect_mongo_operator(path, value):
            return path[0] == "$"

        b = a.collapse(func=detect_mongo_operator)
        self.assertEqual(b, {("k1", "k2"): {"$foo": {("k3", "k4"): "v"}}})

    # _expand

    def test__expand(self):
        a = {("k1", "k2", "k3"): "v"}
        b = NestedDict._expand(a)
        self.assertEqual(b, {"k1": {"k2": {"k3": "v"}}})

    def test__expand__overlapping_paths(self):
        a = {
            ("k1", "k2", "k3"): "v",
            ("k1", "k2", "k4"): "v"
        }
        b = NestedDict._expand(a)
        self.assertEqual(b, {"k1": {"k2": {"k3": "v", "k4": "v"}}})

    def test__expand__nested_class(self):
        a = {("k1",): NestedDict({("k2", "k3"): "v"})}
        b = NestedDict._expand(a)
        self.assertEqual(b, {"k1": {"k2": {"k3": "v"}}})


if __name__ == "__main__":
    unittest.main()
