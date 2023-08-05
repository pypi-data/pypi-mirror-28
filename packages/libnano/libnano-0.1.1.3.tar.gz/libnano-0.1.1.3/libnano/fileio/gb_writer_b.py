import io
import sys
if sys.version_info[0] > 2:
    try:
        import libnano.helpers.textwrap as textwrap
        from libnano.helpers.bytesfmt import bformat
    except:
        # For package imports
        from os.path import join, abspath, dirname
        sys.path.append(abspath(join(dirname(__file__), '..', '..')))
        import libnano.helpers.textwrap as textwrap
        from libnano.helpers.bytesfmt import bformat
else:
    import textwrap
    bformat = lambda x, y: x % y

def write(fd, d, order_qualifiers=False):
    d_info = d[b'info']
    writeLocus(fd, d_info)
    writeDefinition(fd, d_info)
    writeAccession(fd, d_info)
    writeVersion(fd, d_info)
    writeDBLINK(fd, d_info)
    writeKeywords(fd, d_info)
    writeSource(fd, d_info)
    i = 0
    for reference in d_info[b'references']:
        i += 1
        writeReference(fd, reference, i)
    writeComment(fd, d_info)
    writeFeatures(fd, d, order_qualifiers)
    writeOrigin(fd, d)
# end def

def write_file(filepath, d, order_qualifiers=False):
    with io.open(filepath, 'wb') as fd:
        write(fd, d, order_qualifiers=order_qualifiers)
# end def

"""
http://www.insdc.org/files/feature_table.html

section 4.1 shows a 79 character feature table format, as well as the LOCUS
being 80 characters but BioPython files output an 80 character version

However section 4.3 Data item positions shows

    22-80              location

as the 80th character is in play.

This code sticks with 79 character limit
"""

def multiline(main_str, indent_str, lim=67):
    o_list = [ main_str[i:i+lim] for i in range(0, len(main_str), lim) ]
    return indent_str.join(o_list)

def multiline_spaces(main_str, indent_str, lim=67):
    main_list = textwrap.wrap(main_str, lim, drop_whitespace=True,
        break_on_hyphens=False)
    return indent_str.join(main_list)
#end def

def writeLocus(fd, d):
    """
    Locus in sample file is not valid
    """
    locus_str = b"LOCUS       "
    name = d[b'name']
    molecule_type = d[b'molecule_type']
    form = d[b'form']
    if form is None:
        form = b''
    elif form == b'linear':
        form = b'linear  '

    gb_division = d[b'gb_division']
    if gb_division is None:
        gb_division = b''

    mod_date = d[b'mod_date']
    if mod_date is None:
        mod_date = b''

    out_str =  bformat(b"%s%-16s %11d bp    %-6s  %8s %s %s\n" ,
        (locus_str, name, d[b'length'], molecule_type, form, gb_division, mod_date))
    fd.write(out_str)
# end def

def writeDefinition(fd, d):
    definition_str = b"DEFINITION  "
    indent_str = b"\n            "
    out_list = [definition_str,
                multiline_spaces(d[b'definition'], indent_str),
                b'\n']
    fd.write(b''.join(out_list))
# end def

def writeAccession(fd, d):
    accession_str = b"ACCESSION   %s\n"
    fd.write(bformat(accession_str, (d[b'accession'])))
# end def

def writeVersion(fd, d):
    version = d[b'version']
    if version is not None:
        gi = d[b'GI']
        fd.write(bformat(b"VERSION     %s  GI:%s\n", (version, gi) ))
# end def

def writeDBLINK(fd, d):
    if b'dblink' in d:
        if d[b'dblink'] is not None:
            fd.write(bformat(b"DBLINK      %s\n", (d[b'dblink'])))
# end def

def writeKeywords(fd, d):
    keywords_str = b"KEYWORDS    %s\n"
    fd.write(bformat(keywords_str, (d[b'keywords'])))
# end def

def writeSource(fd, d):
    source_str = b"SOURCE      "
    organism_str = b"\n  ORGANISM  "
    indent_str = b"\n            "
    org = d[b'organism']
    out_list = [source_str, d[b'source'],
                organism_str,
                org[0]]
    if org[1] is not None:
        out_list += [   indent_str,
                        multiline_spaces(org[1], indent_str)]
    out_list += [b'\n']
    fd.write(b''.join(out_list))
# end def


def writeReference(fd, ref, i):
    assert(ref[b'r_index'] == i)
    reference_str = b"REFERENCE   "
    authors_str = b"  AUTHORS   "
    title_str = b"  TITLE     "
    indent_str = b"\n            "
    journal_str = b"  JOURNAL   "
    pubmed_str = b"  PUBMED    "
    if ref[b'start_idx'] is not None:
        idx_str = bformat(b"  (bases %d to %d)",
                            (ref[b'start_idx'], ref[b'end_idx']))
    else:
        idx_str = b''
    out_list = [reference_str,
            bformat(b"%d%s\n", (i, idx_str)),
            authors_str,
            multiline_spaces(ref[b'authors'], indent_str), b'\n',
            title_str,
            multiline_spaces(ref[b'title'], indent_str), b'\n',
            journal_str,
            multiline_spaces(ref[b'journal_info'], indent_str), b'\n',
            ]
    if ref[b'pubmed'] is not None:
        out_list += [pubmed_str, ref[b'pubmed'], b'\n']

    fd.write(b''.join(out_list))
# end def

def writeComment(fd, d):
    comment_str = b"COMMENT     "
    indent_str = b"\n            "
    indent_str_gb_asm = b"            "
    if b'comment' in d:
        comment = d[b'comment']
        if isinstance(comment, list):
            out_list = [comment_str,
                multiline_spaces(comment[0], indent_str),
                indent_str, indent_str, indent_str,
                indent_str.join(comment[1]), b'\n'
                ]
        else:
            out_list = [comment_str, multiline_spaces(comment, indent_str), b'\n']
        fd.write(b''.join(out_list))
# end def


def writeFeatures(fd, d, order_qualifiers):
    feature_header = b"FEATURES             Location/Qualifiers\n"
    feature_type_prefix_str = b"     "
    indent_str = b"\n                     "
    feature_type_field_size = 16
    fd.write(feature_header)
    for feature in d[b'features']:
        ftype = feature[b'type']
        location_str = feature[b'location']
        out_list = [feature_type_prefix_str,
                    ftype, (feature_type_field_size - len(ftype))*b" ",
                    location_str, b'\n'
                    ]
        if order_qualifiers:
            quals = feature[b'qualifiers']
            for key in sorted(quals.keys()):
                value_list = quals[key]
                if not isinstance(value_list, list):
                    value_list = [value_list]
                for value in sorted(value_list): # assumes value_list is all the same type
                    if key in (b'codon_start', b'transl_table'):    # codon start is a weird edge case
                        out_list += [bformat(b"                     /%s=%d\n", (key, value))]
                    elif key == b'transl_except':
                        out_list += [bformat(b"                     /%s=%s\n", (key, value))]
                    elif key == b'translation':
                        qualifier_str = bformat(b"/%s=\"%s\"", (key, value))
                        qual_list = multiline(qualifier_str, indent_str, lim=58) # or 58
                        out_list += [b"                     " + qual_list, b'\n']
                    else:
                        if value is None:
                            qualifier_str = bformat(b"/%s\n", (key))
                        else:
                            qualifier_str = bformat(b"/%s=\"%s\"\n", (key, value))
                        qual_list = multiline_spaces(qualifier_str, indent_str, lim=58)  #or 58
                        out_list += [b"                     " + qual_list, b'\n']
        else:
            for key, value_list in feature[b'qualifiers'].items():
                if not isinstance(value_list, list):
                    value_list = [value_list]
                for value in value_list:
                    if key in (b'codon_start', b'transl_table'):    # codon start is a weird edge case
                        out_list += [bformat(b"                     /%s=%d\n", (key, value))]
                    elif key == b'transl_except':
                        out_list += [bformat(b"                     /%s=%s\n", (key, value))]
                    elif key == b'translation':
                        qualifier_str = bformat(b"/%s=\"%s\"", (key, value))
                        qual_list = multiline(qualifier_str, indent_str, lim=58) # or 58
                        out_list += [b"                     " + qual_list, b'\n']
                    else:
                        if value is None:
                            qualifier_str = bformat(b"/%s\n", (key))
                        else:
                            qualifier_str = bformat(b"/%s=\"%s\"\n", (key, value))
                        qual_list = multiline_spaces(qualifier_str, indent_str, lim=58)  #or 58
                        out_list += [b"                     " + qual_list, b'\n']
        fd.write(b''.join(out_list))
# end def

def writeOrigin(fd, d):
    i = 0
    format_string = b'%9d %s %s %s %s %s %s\n'
    origin_header = b"ORIGIN      \n"
    fd.write(origin_header)
    origin = d[b'seq']
    count = len(origin) - 60
    while i < count:
        str_tup = (i+1, ) + tuple([origin[j:j+10] for j in range(i, i+60, 10) ])
        fd.write(bformat(format_string, str_tup))
        i += 60
    last_str = origin[i:]
    last_str = last_str + (60-(len(last_str)))*b" "
    last_list = [last_str[j:j+10] for j in range(0, 60, 10) ]
    last_list = [x.rstrip() for x in last_list if x[0] != b" "[0]]
    str_tup = (i+1, ) + tuple(last_list)
    format_string = b'%9d' + b" %s"*len(last_list) + b'\n'
    fd.write(bformat(format_string, str_tup))
    fd.write(b"//\n")
# end def

if __name__ == '__main__':
    import filecmp
    import gb_reader_b as gbr
    import os.path as opath
    path = opath.dirname(opath.dirname(opath.dirname(opath.abspath(__file__))))
    fn = opath.join(path, "tests", "test_data", "mds42_full.gb")
    # fn = opath.join(path, "tests", "test_data", "sample.gb")

    # fn = opath.join(path, "tests", "test_data", "failed.gb")
    # fn = opath.join(path, "tests", "test_data", "sample_complex.gb")
    fn_out = opath.join(path, "tests", "test_data", "sample_out.gb")
    gbd = gbr.parse(fn, is_ordered=True)
    # print(gbd['references'])
    write_file(fn_out, gbd)
    print(filecmp.cmp(fn, fn_out))
