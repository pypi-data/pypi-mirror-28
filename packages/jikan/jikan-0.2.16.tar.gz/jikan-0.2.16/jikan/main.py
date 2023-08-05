from .mnemonic import MnemonicRef, MnemonicSystem
from etreetools import lib as EL
import re, datetime, os, codecs, csv, itertools, shutil
from urllib.parse import quote_plus
import json
from itertools import chain as ichain, islice
from functools import partial as curry
import operator
from collections import OrderedDict
import xml.etree.ElementTree as ET
from copy import deepcopy
from xml.sax.saxutils import escape as xml_escape
from learnusumjap.re_one_of import re_one_of
from cached_property import cached_property
import pkg_resources

import sqlalchemy as sa
from sqlalchemy.orm import exc, relationship, aliased

from jikan_sqlalchemy_utils.session import SessionMaker
from pyjmdict.db.jmdict import KanjiEntry
from pyjmdict.db.kanjidic import Character
from learnusumjap.explain_reading import (explain_reading_to_html,
                                          explain_reading_helper,
                                          explain_reading_to_html_css)
from learnusumjap.explain_reading_db import ExplainReadingCache
from learnusumjap.kanji_word_examples import (
    Base as KWEBase, WordExample)
from learnusumjap.unicode import CJKUnicodeRanges
from contextlib import closing

from tqdm import tqdm as tqdm_

def unique_iter(iterator, key=id):
    remember = set()
    for e in iterator:
        k = key(e)
        if k not in remember:
            yield e
            remember.add(k)

def itersplit(iterable, n):
    itr = iter(iterable)
    while True:
        r = tuple(islice(itr, n))
        if not r: break
        yield r

cjkur = CJKUnicodeRanges()
cjk_regex_string = cjkur.regex_string()
cjk_re = re.compile('(?:{}|⋏)+'.format(cjk_regex_string))
acceptable_substitutions_file_ext = {'.svg', '.png', '.jpg'}

def parenthesize_if_present(xs, sep=' ', after=' '):
    return ('({}){}'.format(sep.join(xs), after) if len(xs) else '',)

def kanji_entry_html(ke):
    ses = []
    for se in ke.senses:
        gs = [g for g in se.glosses if g.lang=='eng']
        if len(gs):
            ses.append((se, gs))

    r = []
    def add_single(se, gs, counter=None):
        r.extend(parenthesize_if_present(se.parts_of_speech))
        if counter is not None:
            r.append("({}) ".format(counter))
        r.append('; '.join(str(g) for g in gs))
        r.append(' ')

    only_one = len(ses) == 1
    for i, (se, gs) in enumerate(ses, 1):
        add_single(se, gs, None if only_one else i)

    return r

def main():
    import argparse
    parser = argparse.ArgumentParser(
        description=("Generate anki deck and media."),
    )
    default_prefix = 'jikan20171230_'
    parser.add_argument('--source', '-s', required=True, nargs='+',
                        help='source mnemonics.txt')
    parser.add_argument('--substitutions',
                        help='''\
directory containing image files for text substitution''')
    parser.add_argument('--meta-output', required=True,
                        help='where to place "anki.csv"')
    parser.add_argument('--media-output', required=True,
                        help='where to place generated html files')
    parser.add_argument('--prefix', '-p', default=default_prefix, type=str,
                        help='prefix for html files')
    parser.add_argument('--no-details', action='store_true',
                        help="debug option; disable slow features, currently "
                        "just usage examples")
    parser.add_argument('--pyjmdict-db', required=True,
                        help='file containing pyjmdict database URI')
    parser.add_argument('--erc-db', required=True,
                        help='file containing explain-reading-cache '
                        'database URI')
    parser.add_argument('--kwe-db', required=True,
                        help='file containing kanji-word-examples '
                        'database URI')
    args = parser.parse_args()

    assert os.path.isdir(args.meta_output)
    assert os.path.isdir(args.media_output)
    assert os.path.isdir(args.substitutions)
    media_dir = args.media_output
    output_csv_path = os.path.join(args.meta_output, 'output.csv')

    ms = MnemonicSystem([open(f) for f in args.source])
    assocs = ms.assocs

    with open(os.path.join(
        args.meta_output, 'debug_dump.txt'), 'wt') as handle:
        for ass in assocs:
            if ass.has_rhs:
                print(str(ass), file=handle)

    with pkg_resources.resource_stream(
            __name__, 'data/Heisigs_RTK_6th.json') as handle:
        heisig = json.loads(handle.read().decode('utf8'))
    with open(os.path.join(
            args.meta_output, 'debug_report.txt'), 'wt') as handle:
        pr = curry(print, file=handle)
        heisig_changed = []
        heisig_completed = 0
        for index, item, heisig_keyword in heisig:
            label = ms.main_label.get(item)
            if label:
                heisig_completed += 1
                if label != heisig_keyword:
                    heisig_changed.append((item, heisig_keyword, label))
        pr("Heisig kanji completed: {}/{}".format(heisig_completed, len(heisig)))
        pr()
        pr("Heisig kanji with changed keywords:", file=handle)
        for item, heisig_keyword, label in heisig_changed:
            pr('  {}: {} --> {}'.format(item, heisig_keyword, label))
        pr()
        pr('Items missing stories:')
        for item in ms.i2l:
            if item not in ms.main_label:
                llassocs = ms.i2l2a[item].items()
                if not len(llassocs): continue
                pr('  {}: {}'.format(item, ', '.join(
                    '{!r}'.format(label)
                    for label, lassocs in sorted(llassocs))))

    igroup = OrderedDict(
        ('g{}'.format(i), tuple(items))
        for i, items in enumerate(itersplit(ms.i2l, 10)))

    pyjmdict_sessionmaker = SessionMaker.from_uri_filename(
        args.pyjmdict_db)

    erc = ExplainReadingCache(
        cache_sessionmaker=SessionMaker.from_uri_filename(
            args.erc_db, isolation_level='READ COMMITTED'))

    kwe_sm = SessionMaker.from_uri_filename(
        args.kwe_db)

    gen = HtmlGenerator(
        mnemonic_system=ms,
        filename_prefix=args.prefix,
        media_output_directory=args.media_output,
        item_group_dict=igroup,
        pyjmdict_sessionmaker=pyjmdict_sessionmaker,
        explain_reading_cache=erc,
        kanji_word_example_sessionmaker=kwe_sm,
        no_details=args.no_details)

    gen.init_substitutions(args.substitutions)

    gen.write_anki_files()

    gen.write_anki_csv(open(os.path.join(
        args.meta_output, 'anki.csv'), 'w'))

class HtmlGenerator:
    def __init__(self, mnemonic_system, filename_prefix,
                 media_output_directory, item_group_dict,
                 pyjmdict_sessionmaker,
                 explain_reading_cache,
                 kanji_word_example_sessionmaker,
                 no_details):
        self.substitutions = {}
        self.media_list = []
        self.filename_prefix = filename_prefix
        self.media_output_directory = media_output_directory
        self.item_group_dict = item_group_dict
        self.mnemonic_system = mnemonic_system
        self.pyjmdict_sessionmaker = pyjmdict_sessionmaker
        self.explain_reading_cache = explain_reading_cache
        self.kanji_word_example_sessionmaker = kanji_word_example_sessionmaker
        self.no_details = no_details

    def init_substitutions(self, substitutions_directory):
        substitutions = self.substitutions
        media_list = self.media_list
        for root, _, files in os.walk(substitutions_directory):
            for f in files:
                text, ext = os.path.splitext(f)
                if ext not in acceptable_substitutions_file_ext:
                    continue
                try:
                    sub_type, text = text.split('_')
                    text = codecs.decode(text, 'hex').decode('utf-8')
                except:
                    continue
                new_f = self.filename_prefix+f
                substitutions[text] = (sub_type, new_f)
                media_list.append(new_f)
                shutil.copyfile(
                    os.path.join(root, f),
                    os.path.join(self.media_output_directory, new_f))
        self.substitutions_re = re.compile(re_one_of(substitutions.keys()))

    @cached_property
    def item_to_item_group_dict(self):
        return {item: item_group
                for item_group, items in self.item_group_dict.items()
                for item in items}

    def get_item_group_filename(self, item_group):
        return '{}{}.html'.format(
            self.filename_prefix, codecs.encode(
                item_group.encode('utf-8'), 'hex').decode('ascii'))

    def get_item_fragment(self, item, label=None):
        return item + '--' + label if label else item

    def get_item_url(self, item, label=None):
        d = self.item_to_item_group_dict
        return '#'.join((
            quote_plus(self.get_item_group_filename(d[item])),
            quote_plus(self.get_item_fragment(item, label))))

    @cached_property
    def one_of_items_regex(self):
        return re.compile(re_one_of(self.item_to_item_group_dict.keys()))

    def htmltrans_item_links(self, tag):

        def callback(matchobj):
            item = matchobj.group()
            a = ET.Element('a', attrib={
                'href': self.get_item_url(item)})
            a.text = item
            return [a]

        def recur(tag):
            if tag.tag == 'a' and 'href' in tag.attrib:
                return

            for child in tag:
                recur(child)

            EL.transform_text(
                tag,
                curry(EL.regex_sub_e_iter, self.one_of_items_regex, callback))

        recur(tag)

        return tag

    def htmltrans_cjk(self, tag):
        def callback(matchobj):
            text = matchobj.group()
            span = ET.Element('span', attrib={'lang': 'ja', 'class': 'cjk'})
            span.text = text
            return [span]

        def recur(tag):
            if (tag.tag == 'span' and
                tag.attrib.get('lang') and
                'cjk' in tag.attrib.get('class', '').split()):
                return

            for child in tag:
                recur(child)

            EL.transform_text(
                tag,
                curry(EL.regex_sub_e_iter, cjk_re, callback))

        recur(tag)

        return tag

    def htmltrans_cjk_zoom(self, tag):
        def recur(tag):
            if (tag.tag == 'span' and
                tag.attrib.get('lang') and
                'cjk' in tag.attrib.get('class', '').split()):
                tag.attrib['class'] += ' cjkz'

            if tag.tag == 'ruby':
                tag.attrib['class'] = (tag.attrib.get('class', '') + ' cjkz')
                return # no recurse

            for child in tag:
                recur(child)

        recur(tag)

        return tag

    def htmltrans_substitutions(self, tag):
        substitutions = self.substitutions
        substitutions_re = self.substitutions_re

        def substitutions_callback(matchobj):
            k = matchobj.group()
            sub_type, sub_file = substitutions[k]
            if sub_type == 'kc':
                img = ET.Element('img', src=sub_file, alt=k)
                img.attrib['class'] = 'subst-kc'
                return [img]
            else:
                raise ValueError(
                    "unrecognized substitution type {!r} on {!r}".format(
                        sub_type, k))

        for t in tuple(tag.iter()):
            EL.transform_text(
                t,
                curry(EL.regex_sub_e_iter,
                      substitutions_re,
                      substitutions_callback))

        return tag

    def htmlspan(self, string):
        try:
            return ET.fromstring('<span>{}</span>'.format(string))
        except:
            raise ValueError("ET error on {!r}".format(string))

    def htmltrans_mnemonic(self, tree):
        self.htmltrans_substitutions(tree)
        self.htmltrans_cjk(tree)
        self.htmltrans_cjk_zoom(tree)
        return tree

    def generate_association_html(self, ass, anki=False):
        P = self.htmlspan
        trans = self.htmltrans_mnemonic
        def callback(e):
            if isinstance(e, MnemonicRef):
                display_label = e.display_label
                display_label = (e.label if display_label is None
                                 else display_label)
                e_a1 = ET.Element('a')
                e_a1.attrib['href'] = self.get_item_url(e.item)
                e_a2 = ET.Element('a')
                e_a2.attrib['href'] = self.get_item_url(e.item, e.label)
                EL.extend_with_children_of(e_a1, trans(P(e.item)))
                EL.extend_with_children_of(e_a2, trans(P(display_label)))
                return ['(', e_a1, ')', e_a2]
            else:
                return EL.unwrap(trans(P(e)))
        return ichain.from_iterable(map(callback, ass.rhs))

    def generate_association_html_li(self, ass, **kwargs):
        li = ET.Element('li')
        EL.extend(li, self.generate_association_html(ass, **kwargs))
        return li

    @cached_property
    def orig_et(self):
        orig_et = ET.fromstring('''\
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
  "http://www.w3.org/TR/xhtml1/DTD/strict.dtd">
<html>
<head><meta charset="utf-8" />
<link rel="stylesheet" type="text/css" href="{}" />
</head>
<body></body></html>'''.format(self.filename_prefix+'style.css'))
        return orig_et

    def gen_css(self):
        jikan_css = '''\
@font-face {
  font-family: "Noto Sans CJK JP";
  font-style: normal;
  font-weight: 400;
  src: local("Noto Sans CJK JP"),
         url("_NotoSansCJKjp-Regular.woff") format("woff"),
    url("jikan_NotoSansCJKjp-Regular.woff") format("woff");
}

body, .card {
  /* stolen from jisho.org */
  font-family: "Helvetica Neue", Helvetica, Arial, HiraKakuProN-W3, "Hiragino Kaku Gothic ProN W3", "Hiragino Kaku Gothic ProN", "ヒラギノ角ゴ ProN W3", メイリオ, Meiryo, 游ゴシック, YuGothic, "ＭＳ Ｐゴシック", "MS PGothic", "ＭＳ ゴシック", "MS Gothic", sans-serif;
}

.card {
  font-size: 20px;
  color: black;
  background-color: white;
}

.card-keyword {
  text-align: center;
}

.card-kanji {
  text-align: center;
  font-size: 25px;
}

.card-story {
  text-align: left;
  font-size: 16px;
}

.cjk {
  /* stolen from jisho.org */
  font-family: "Noto Sans CJK JP", HiraKakuProN-W3, "Hiragino Kaku Gothic ProN W3", "Hiragino Kaku Gothic ProN", "ヒラギノ角ゴ ProN W3", メイリオ, Meiryo, 游ゴシック, YuGothic, "ＭＳ Ｐゴシック", "MS PGothic", "ＭＳ ゴシック", "MS Gothic", sans-serif;
  font-weight: 400;
  font-style: normal;
}

.cjkz {
  font-size:200%;
  color:black;
}

.subst-kc {
  vertical-align:text-bottom;
  height:1.8em;
}

a {
  text-decoration:none;
}

hr.item-sep {
  border-top: 3px double #888;
}

ul.kanji-reading {
  list-style: none;
  padding: 0px;
}

ul.kanji-reading li:before {
  content: '-';
  margin: 0 0.4em 0 0.2em;
}

'''
        return jikan_css+'\n\n'+explain_reading_to_html_css()

    def add_extra_item_info(self, item, body):
        div = ET.SubElement(body, 'div', attrib={
            'class': 'extra-info'})

        if self.no_details:
            return

        erc = self.explain_reading_cache

        # TODO: make it possible to manually override given examples
        WE = aliased(WordExample, name='WE')
        with closing(self.kanji_word_example_sessionmaker()) as S:
            kwes = list(S.query(WE).filter(WE.kanji == item).all())

        KE = aliased(KanjiEntry, name='KE')
        with closing(self.pyjmdict_sessionmaker()) as S:
            char = S.query(Character).get(item)
            if char is not None:
                readings = tuple(unique_iter(
                    (r for rm in char.rms for r in rm.readings),
                    key=lambda r: r.str))
                ul = ET.SubElement(div, 'ul', attrib={
                    'class': 'kanji-reading'})
                li = ET.SubElement(ul, 'li')
                EL.extend(li, ('kun: ', ', '.join(
                    r.str for r in readings if r.type == 'ja_kun')))
                li = ET.SubElement(ul, 'li')
                EL.extend(li, ('on: ', ', '.join(
                    r.str for r in readings if r.type == 'ja_on')))

            for kwe in kwes:
                word = kwe.word
                word_reading = kwe.reading

                p = ET.SubElement(div, 'p')
                EL.extend(p, explain_reading_to_html(
                    erc(S, word, word_reading)))
                EL.extend(p, (' ',))
                ke = S.query(KE).filter(KE.str == word).first()
                EL.extend(p, kanji_entry_html(ke))

        self.htmltrans_item_links(div)

    def generate_items_page(self, items):
        P = self.htmlspan
        trans = self.htmltrans_mnemonic
        ms = self.mnemonic_system

        et = deepcopy(self.orig_et)
        body = et.find('body')

        for item in items:
            ET.SubElement(body, 'a', attrib={
                'name': self.get_item_fragment(item)})
            h3 = ET.SubElement(body, 'h3')
            EL.extend_with_children_of(h3, trans(P(item)))

            ul = ET.SubElement(body, 'ul')

            for ass in unique_iter(ms.lhsi2a[item]):
                ul.append(self.generate_association_html_li(ass))

            if not len(ul): body.remove(ul)

            self.add_extra_item_info(item, body)

            ET.SubElement(body, 'hr')

            for label, lassocs in sorted(ms.i2l2a[item].items()):
                ET.SubElement(body, 'a', attrib={
                    'name': self.get_item_fragment(item, label)})
                h3 = ET.SubElement(body, 'h3')
                EL.extend_with_children_of(h3, trans(P(item+': '+label)))
                label_ul = ET.SubElement(body, 'ul')
                for ass in unique_iter(lassocs):
                    label_ul.append(self.generate_association_html_li(ass))

            ET.SubElement(body, 'hr', attrib={'class': 'item-sep'})

        self.htmltrans_cjk(body)

        return ET.tostring(et, encoding='unicode')

    def media_filename(self, filename):
        self.media_list.append(filename)
        return os.path.join(self.media_output_directory, filename)

    def write_anki_files(self):
        mf = self.media_filename

        autogen_msg = 'autogenerated by https://hydra.bacontoast.org/f/jikan/'
        autogen_msg_css = "/* {} */\n\n".format(autogen_msg)

        css_fn = self.filename_prefix + 'style.css'
        with open(mf(css_fn), 'wt') as handle:
            handle.write(autogen_msg_css)
            handle.write(self.gen_css())

        acss_fn = self.filename_prefix + 'style_anki.css'
        with open(mf(acss_fn), 'wt') as handle:
            handle.write(autogen_msg_css)
            handle.write('@import "{}"\n\n'.format(css_fn))

        for item_group, items in tqdm_(self.item_group_dict.items()):
            filename = self.get_item_group_filename(item_group)

            with open(mf(filename), 'wt') as handle:
                handle.write(self.generate_items_page(items))

    def write_anki_csv(self, file):
        def _html(s):
            tree = self.htmlspan(s)
            self.htmltrans_mnemonic(tree)
            return ET.tostring(tree, 'unicode')

        ms = self.mnemonic_system

        writer = csv.writer(file)
        counter = 0
        def writerow(item, label, story):
            nonlocal counter
            counter += 1
            # Key, Kanji, Label, Story, Counter
            writer.writerow([xml_escape(item), _html(item),
                             _html(label), story, counter])
        for item in tqdm_(ms.item_order):
            if True and (len(item) > 1 and item not in self.substitutions):
                raise ValueError("long item {!r}".format(item))
            iassocs = ms.lhsi2a.get(item, None)
            if iassocs is None or not len(iassocs): continue
            label = ms.main_label[item]
            container = ET.Element('div')
            ul = ET.SubElement(container, 'ul')
            for ass in unique_iter(iassocs):
                ul.append(self.generate_association_html_li(
                    ass, anki=True))
            self.add_extra_item_info(item, container)
            self.htmltrans_cjk(container)
            writerow(item, label, ET.tostring(container, encoding='unicode'))

        # create media reference cards to tell anki about the html files
        # the grouper is necessary because of field size limit on csv
        for i, ml in enumerate(itersplit(self.media_list, 300)):
            mediaref_key = '__MEDIAREF:{}__'.format(i)
            writerow(mediaref_key, mediaref_key, '''\
This is an empty card used to reference all the attached files. Feel
free to disable it.<br/> <div style="display:none;">{}</div>'''.format(
    ' '.join('[sound:{}]'
             .format(f) for f in ml)))

main()
