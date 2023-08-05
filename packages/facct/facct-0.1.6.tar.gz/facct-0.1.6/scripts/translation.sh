#!/bin/bash
script_root=$(dirname $0)
app_root=$(dirname $script_root)
export PYTHONPATH=$PYTHONPATH:$app_root
py_root=$(dirname $(ls $app_root/*/config.py))
domain=$(basename $py_root)
lang=fr
country=FR
encoding=UTF-8
LC=${lang}_${country}
po_dir=$app_root/po
mo_dir=$py_root/locale/$LC/LC_MESSAGES

if [ "$1" = "update" ]; then
    env PWD=$py_root xgettext --language=Python --keyword=_ --output=- \
            `find . -name "*.py"`| grep -v '^#'| \
            sed "s+\(charset\)=CHARSET+\1=${encoding}+;s+\(Language:\) +\1 $lang+" \
            > $app_root/po/$domain.pot

    if [ -f $po_dir/$lang.po ]; then
        cp $po_dir/$lang.po $po_dir/$lang.po.bkup
        msgmerge --sort-output --update --no-fuzzy-matching --backup=off -i $po_dir/$lang.po $po_dir/$domain.pot
        if [ ! $? -eq 0 ]; then
            echo "Error while updating PO file, rolling back" >&2
            cp $po_dir/$lang.po.bkup $po_dir/$lang.po
        fi
    else
        msginit -i $po_dir/$domain.pot --locale=$LC -o $po_dir/$lang.po --no-translator
    fi
fi

mkdir -p $mo_dir
msgfmt $po_dir/$lang.po -o $mo_dir/$domain.mo --check-domain
#iconv $po_dir/$lang.po -t=ISO-8859-1 -f=UTF-8 > $po_dir/$lang-utf8.po

# runtime test:
account_dir=$py_root/bench_infra/corp_ref/accounts/2013
env LANG=$LC.$encoding python $py_root/generate_all.py -o corp_ref -d $account_dir
env LANG=$LC.$encoding python3 $py_root/generate_all.py -o corp_ref -d $account_dir
env LANG=$LC.$encoding python $py_root/bill/gen_tex.py -o corp_ref 022013.csv
env LANG=$LC.$encoding python3 $py_root/bill/gen_tex.py -o corp_ref 022013.csv
