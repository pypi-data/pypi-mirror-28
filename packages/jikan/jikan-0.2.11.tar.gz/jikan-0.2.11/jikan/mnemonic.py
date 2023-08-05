import re
from collections import OrderedDict, defaultdict
from cached_property import cached_property
from generic_escape import GenericEscape
from itertools import chain as iterchain

class NamedIndex(object):
    def __init__(self, index):
        self.index = index

    def __get__(self, obj, objtype):
        return obj.data[self.index]

    def __set__(self, obj, value):
        obj.data[self.index] = value

# [item-or-alias|]
# [|label]
# [...|...|displaylabel]
# [...|...|...|alias] (alias definition)
class MnemonicRef:
    def __init__(self, value=None, **kwargs):
        if value is None:
            value = ()

        value = list(value)
        value.extend((None,)*(4 - len(value)))
        self.data = value

        for k, v in kwargs:
            setattr(k, v)

    def __iter__(self):
        return iter(self.data)

    def __str__(self):
        i = next(j for j, v in reversed(tuple(enumerate(self)))
                 if v is not None)
        escape = text_association_escape.escape
        return '|'.join([escape(x if x else '') for x in self.data[0:i+1]])

    item          = NamedIndex(0)
    label         = NamedIndex(1)
    display_label = NamedIndex(2)
    alias         = NamedIndex(3)

    @property
    def is_empty(self):
        return self.item is None and self.label is None

    def __repr__(self):
        return '<MnemonicRef {!r}>'.format(str(self))

def concatenate_adjacent_strings(iterator):
    a = []
    for e in iterator:
        if isinstance(e, str):
            a.append(e)
        else:
            s = ''.join(a)
            a.clear()
            if s: yield s
            yield e
    s = ''.join(a)
    if s: yield s

class TextAssociationEscape(GenericEscape):
    escaped = {
        "\\": r"\\",
        "[":  r"\[",
        "]":  r"\]",
        "|":  r"\|",
        "\n": r"\n"}
text_association_escape = TextAssociationEscape()

class BaseAssociation:
    def __init__(self, lhs, rhs):
        self.lhs = list(lhs)
        self.rhs = list(rhs)

    @classmethod
    def from_string(cls, text, *args, **kwargs):
        r = []
        in_bracket = []
        k = 0
        mode = 'text'

        while True:
            k, unescaped_string = text_association_escape.unescape(
                text, start_position=k)

            if mode == 'text':
                r.append(unescaped_string)

            if k == len(text):
                if mode != 'text':
                    raise ValueError("syntax error")
                break

            c = text[k]
            if c == '[':
                if mode != 'text':
                    raise ValueError("syntax error")
                mode = 'bracket'
                k += 1
            elif c == '|' or c == ']':
                if mode != 'bracket':
                    raise ValueError("syntax error")
                in_bracket.append(unescaped_string)
                if c == ']':
                    r.append(MnemonicRef(tuple(
                        (None if x=='' else x) for x in in_bracket)))
                    in_bracket.clear()
                    mode = 'text'
                k += 1
            else:
                raise ValueError("syntax error")

        if r[0] == '':
            del r[0]
        first = r[0]
        for i, ref in enumerate(r):
            if isinstance(ref, MnemonicRef):
                if ref.is_empty:
                    ref.item  = first.item
                    ref.label = first.label

        r = tuple(concatenate_adjacent_strings(iter(r)))
        lhs_count = next(i for i, v in enumerate(iterchain(r, (None,)))
                         if not isinstance(v, MnemonicRef))
        lhs = r[:lhs_count]
        rhs = r[lhs_count:]

        return cls(lhs, rhs, *args, **kwargs)

    def invalidate(self):
        s = self
        del s.lhs_count, s.refs, s.rhs_refs, s.has_rhs

    @cached_property
    def lhs_count(self):
        return len(self.lhs)

    @cached_property
    def refs(self):
        return tuple(self.lhs) + self.rhs_refs

    @cached_property
    def rhs_refs(self):
        return tuple(x for x in self.rhs if isinstance(x, MnemonicRef))

    def __str__(self):
        return ''.join(
            '[{}]'.format(str(x)) if isinstance(x, MnemonicRef) else x
            for x in iterchain(self.lhs, self.rhs))

    @cached_property
    def has_rhs(self):
        return len(self.rhs) > 0

    def __repr__(self):
        return "<A {!r}>".format(str(self))

class AssociationWithSource(BaseAssociation):
    def __init__(self, *args, source_filename=None, source_line=None, **kwargs):
        self.source_filename = source_filename
        self.source_line = source_line
        try:
            super().__init__(*args, **kwargs)
        except Exception as exc:
            raise RuntimeError("error processing association {}"
                               .format(self.get_source())) from exc

    def get_source(self):
        return '{!r}:{}'.format(self.source_filename, self.source_line)

    @classmethod
    def from_string_with_source(
            cls, *args, source_filename=None, source_line=None, **kwargs):
        try:
            return cls.from_string(*args, **kwargs)
        except Exception as exc:
            raise RuntimeError("error initializing association {!r}:{}"
                               .format(source_filename, source_line)) from exc

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if exc_value is not None:
            raise RuntimeError("error processing association {!r} at {}"
                               .format(self, self.get_source())) from exc_value

class MnemonicSystem:
    association_class = AssociationWithSource
    def __init__(self, fileobjs=None):
        self.alias2m = dict()
        self.assocs = []
        if fileobjs is not None:
            for file in fileobjs:
                self.add_file(file)
            self.expand_aliases()
            self.process()

    def add_file(self, file):
        filename = file.name
        self.assocs.extend(AssociationWithSource.from_string_with_source(
            line.strip(), source_filename=filename, source_line=i)
                           for i, line in enumerate(file, 1))

    def expand_aliases(self):
        alias2m, assocs = self.alias2m, self.assocs
        for ass in self.assocs:
            for m in ass.refs:
                a = m.alias
                if a is not None:
                    if a in alias2m:
                        raise ValueError("cannot redefine alias {!r} at {}"
                                         .format(a, ass.get_source()))
                    alias2m[a] = m

        for ass in assocs:
            for m in ass.refs:
                alias_m = alias2m.get(m.item)
                if alias_m is not None:
                    m.item = alias_m.item
                    for field in ('label', 'display_label'):
                        if getattr(m, field) is None:
                            setattr(m, field, getattr(alias_m, field))

    def process(self):
        assocs = self.assocs
        # resolve missing item or label
        self.i2l = i2l = OrderedDict()
        self.l2i = l2i = OrderedDict()

        for ass in assocs:
            for m in ass.refs:
                i, l = m.item, m.label
                if i is not None and l is not None:
                    if i not in i2l:
                        i2l[i] = l
                    if l not in l2i:
                        l2i[l] = i

        for ass in assocs:
            for m in ass.refs:
                try:
                    if m.item is None:
                        m.item = l2i[m.label]
                    if m.label is None:
                        m.label = i2l[m.item]
                except KeyError as e:
                    raise KeyError("KeyError on {!r} at {}".format(
                        str(m), ass.get_source())) from e

        def itemset(refs):
            return set(r.item for r in refs if isinstance(r, MnemonicRef))

        self.item_order = item_order = OrderedDict()
        self.lhsi2a = lhsi2a = defaultdict(list)
        self.i2l2a  = i2l2a  = defaultdict(lambda:defaultdict(list))
        for ass in assocs:
            with ass:
                if ass.has_rhs:
                    for m in ass.refs:
                        i2l2a[m.item][m.label].append(ass)
                    for m in ass.lhs:
                        item_order[m.item] = True
                        lhsi2a[m.item].append(ass)
                    lhs_only = itemset(ass.lhs).difference(
                        itemset(ass.rhs_refs))
                    if len(lhs_only):
                        raise ValueError(
                            "ref only in LHS {!r}".format(
                                lhs_only))

        main_label = self.main_label = dict()
        labels_entered = set()
        for item in item_order:
            iassocs = lhsi2a.get(item, None)
            if iassocs is None or not len(iassocs): continue
            label = next(r.display_label or r.label
                         for r in iassocs[0].refs
                         if r.item == item)
            if label in labels_entered:
                raise ValueError("duplicate label {!r} on {!r}".format(
                    label, item))
            main_label[item] = label
            labels_entered.add(label)
