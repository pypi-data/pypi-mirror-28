#!/usr/bin/python
#-*- coding: utf-8 -*-

# Copyright (c) 2013 Eric F <efigue> Figerson
# Author(s):
#   Eric F <eric.foss@free.fr>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import sys
import csv
import time
import calendar
import decimal
import shutil
import subprocess
import locale
import re
import glob
import datetime
import platform
import facct.config as config
from facct.i18n import _

def setlocale():
    local_name = 'fr_FR.UTF-8'
    if platform.os.name == 'nt':
       #See: http://msdn.microsoft.com/en-us/library/cdax410z%28VS.71%29.aspx
       local_name = 'fra_fra'
       if 'fr_fr' in locale.locale_alias:
           locale.setlocale(locale.LC_ALL, local_name)
    else:
        if local_name.split('.')[0].lower() in locale.locale_alias:
            locale.setlocale(locale.LC_ALL, local_name)
setlocale()


def get_float(str):
    if str:
        if str == '-':
            return 0
        return decimal.Decimal(str.replace(',', '.'))
    else:
        return decimal.Decimal(0)

def filename_info(csv_file_name):
    base_name = os.path.basename(csv_file_name).split('.')[0]
    if len(base_name)<6:
        sys.stderr.write(_('No correct input file name (eg. 012011.csv)\n'))
        sys.exit(2)
    month = int(''.join(base_name[0:2]))
    year = int(''.join(base_name[2:]))
    return year, month

def next_entry(reader):
    for r in reader: return r
    return []

def load_entries(csv_file_name):
    reader = csv.reader(open(csv_file_name, 'r'), delimiter=';', quotechar='"')
    dico_prestation = {}
    year, month = filename_info(csv_file_name)
    for week in calendar.monthcalendar(year, month):
        r = next_entry(reader)
        dico_prestation.update(zip(week, r))
    return year, month, dico_prestation

def check_output(p):
    if p.stderr:
        if p.stdout:
            print (''.join(p.stdout))
        print (''.join(p.stderr))
    return (0 == p.returncode)

def gen_dvi(dico):
    if not parse_latex(dico):
        return False
    if os.path.exists(dico['root_file'] + '.toc'):
        if not parse_latex(dico):
            return False
    print (_('%(base_file)s.dvi generated.') % dico)
    return True

def parse_latex(dico):
    if not os.path.exists(dico['root_file'] + '.tex'):
        sys.stderr.write(_('%(root_file)s.tex: file not found\n') % dico)
        sys.exit(2)
        return False
    p = subprocess.Popen('latex -version', shell=True, stdout=subprocess.PIPE)
    p.communicate()
    if p.returncode:
        sys.stderr.write(_('latex command not found, please install it.\n'
            '\t MikTeX on Windows,\n'
            '\t texlive-latex on RPM based Linux distributions\n'
            '\t or texlive-latex-base texlive-lang-french texlive-latex-extra'
            ' texlive-fonts-recommended'
            '\t for Debian based distributions (like Ubuntu)\n'))
        return False
    p = subprocess.Popen('latex -halt-on-error %(base_file)s.tex' % dico,
        cwd=dico['tmp_dir'], shell=True, stdout=subprocess.PIPE)
    p.communicate()
    rc = check_output(p)
    if p.stdout:
        p.stdout.close()
    if not rc:
        log_file = dico['root_file'] + '.log'
        if os.path.exists(log_file):
            for l in open(log_file, 'rb'):
                print (l)
        sys.exit(2)
    return True

def gen_pdf(dico):
    if not os.path.exists(dico['root_file']+'.dvi'):
        sys.stderr.write(_('%(root_file)s.dvi: file not found\n') % dico)
        sys.exit(2)
        return False
    pdf_file = os.path.join('%(target_dir)s', '%(base_file)s.pdf')
    if platform.os.name == 'nt':
        cmd = 'dvipdfm %(root_file)s.dvi -o ' + pdf_file
    else:
        cmd = 'dvipdf %(root_file)s.dvi ' + pdf_file
    p = subprocess.Popen( cmd % dico, shell=True, stdout=subprocess.PIPE)

    p.communicate()
    rc = check_output(p)
    p.stdout.close()
    if not rc:
        sys.stderr.write(_('Fatal error while generating PDF file %s.') % (
                    pdf_file % dico))
        sys.exit(2)
    print (_('%(base_file)s.pdf generated.') % dico)

def get_DocTC_params(orga, year, type_doc):
    target_dir = os.path.join( config.get_accounts_dir(orga),
            '%s' % year, 'tribunal_commerce')
    doc_tmpl = 'Annexe' if (type_doc == DocTC.ANNEXE) else 'Bilan_CExploit'
    dico = { 'target_dir':target_dir,
        'company_name' : Company(orga)['Name'],
        'tmp_dir' : os.path.join(target_dir, 'tmp'),
        'document_tmpl' : '%s_tmpl' % doc_tmpl,
        'year' : year,
        'file_type' : DocTC.doc_names[type_doc].replace(' ', '_'),
    }
    dico['base_file'] = '%(file_type)s_%(year)s_%(company_name)s' % dico
    dico['root_file'] = os.path.join(dico['tmp_dir'], dico['base_file'])
    return dico

def get_bill_params(orga, year, month, company_name):
    bills_dir = get_bills_dir(orga)
    target_dir = os.path.join(bills_dir, str(year))
    tmp_dir = os.path.join(bills_dir, 'tmp')
    id_bill = '0'*(2-len(str(month))) + '%d%d' % (month, year)
    dico = { 'target_dir':target_dir,
        'id_bill' : id_bill,
        'company_name' : company_name,
        'tmp_dir' : tmp_dir,
        'document_tmpl' : 'Facture_GEN_company_client',
    }
    dico['base_file'] = 'Facture_%(id_bill)s_%(company_name)s' % dico
    dico['root_file'] = os.path.join(dico['tmp_dir'], dico['base_file'])
    return dico

def write_pdf(params, unicode_TeX):
    tmp_dir = params['tmp_dir']
    target_dir = params['target_dir']
    if not os.path.isdir(tmp_dir):
        os.makedirs(tmp_dir)
    if not os.path.isdir(target_dir):
        os.mkdir(target_dir)

    parameters_file = os.path.join(tmp_dir, 'data_parameters.tex')
    open(parameters_file, 'w').write(unicode_TeX)
    tmpl_file = os.path.join(config.get_internal_data_dir(),
            '%(document_tmpl)s.tex' % params)
    if not os.path.exists(tmpl_file):
        sys.stderr.write(_('%s: file not found\n') % tmpl_file)
        sys.exit(2)
    base_file_name = os.path.join(tmp_dir, '%(base_file)s.tex' % params)
    shutil.copyfile(tmpl_file, base_file_name)
    print (_('%(base_file)s.tex generated.') % params)

    if gen_dvi(params):
        gen_pdf(params)

    shutil.rmtree(tmp_dir)

def getDate(val):
    return datetime.datetime(*(time.strptime(val, '%Y/%m/%d')[0:6])).date()

def getSameDayNextMonth(date):
    return datetime.date(date.year + date.month//12,
            (date.month % 12) + 1, date.day)

def get_bills_dir(orga):
    return  config.get_bills_dir(orga)

def get_reader(orga, csv_file_name):
    csv_file = os.path.join(config.get_data_dir(orga), csv_file_name)
    if not os.path.exists(csv_file):
        sys.stderr.write(_('%s does not exist\n') % csv_file)
        sys.exit(2)
    return csv.reader(open(csv_file, 'r'), delimiter=';', quotechar='"')

class DocTC:
    BILAN, COMPTE_RESULTAT, ANNEXE = range(3)
    doc_names = ('BILAN', 'COMPTE DE RESULTAT', 'ANNEXE')
    def __init__(self, orga, type_doc, year):
        self._orga = orga
        self._type_doc = type_doc
        self._year = year
        self._lines = []

    def structure_tableau(self):
        if self._type_doc == DocTC.BILAN:
            return r'''
    |P{2.1in}|P{0.7in}|P{0.75in}|P{0.7in}|P{0.7in}|P{2.1in}|P{0.7in}|P{0.7in}|}
    \hline
    \multicolumn{5}{|P{4.85in}|}{\centering{\textbf{ACTIF}}} &
    \multicolumn{3}{P{3.5in}|}{\centering{\textbf{PASSIF}}}
    \\\hline
    Descriptif &
    Brut & \scriptsize{Amortissement/ Dépréciations} & Net & Exercice %(prev_year)s&
    Descriptif &
    Valeur & Exercice %(prev_year)s
    \\\hline''' % { 'prev_year' : self._year - 1, }
        else:
            return r'''
    |P{2.555in}|P{0.8in}|P{0.8in}|P{2.555in}|P{0.8in}|P{0.8in}|}
    \hline
    \multicolumn{3}{|P{4.155in}|}{\centering{\textbf{CHARGES (hors taxes)}}} &
    \multicolumn{3}{P{4.155in}|}{\centering{\textbf{PRODUITS (hors taxes)}}}
    \\\hline
    Descriptif &
    Exercice %(year)s & Exercice %(prev_year)s&
    Descriptif &
    Exercice %(year)s & Exercice %(prev_year)s
    \\\hline''' % { 'year' : self._year, 'prev_year' : self._year - 1, }

    def get_row_tex(self, left, right):
        def f(r):
            if r: return r
            return '~'

        def nb(r):
            if not r.strip(): return r
            if r == '0.00': return '~'
            return r'\raggedleft{$%s$}' % r.replace('.', ',')

        def bold(v):
            if v.lower().startswith('total') or \
                v.endswith('I)') or v.endswith('V)'):
                return r'\textbf{%s}' % v
            return v

        for i, v in enumerate(left[1:]):
            left[i+1] = nb(left[i+1])
        right[-2] = nb(right[-2])
        if right[-1].strip():
            if right[-1].strip() == '0.00':
                right[-1] = '~'
            else:
                right[-1] = r'\rlt{$%s$}' % right[-1].replace('.', ',')
        left[0] = bold(left[0])
        right[0] = bold(right[0])
        complete_row = left + right
        return '&'.join([f(r) for r in complete_row]) + r'\\\hline'

    def append(self, left, right):
        self._lines.append(self.get_row_tex(left, right))

    def add_header_company(self, title):
        company = Company(self._orga)
        return r'''
        %(macros_company)s
        \gdef\FacctYear{%(year)s}
        \gdef\GenYear{%(gen_year)s}
        \gdef\DocTitle{%(TITLE)s}
        \newcommand\companyHeader{
        {\textbf{\companyName}} \par
        \companyCompanyLongForm\ au capital de \companyCapital\ euros\par
        Siège social: \companyShortAddress \companySuffixAddress\par
        \companySiren\ R.C.S. \companyRCS } ''' % {
                'year' : self._year,
                'gen_year' : self._year + 1,
                'macros_company' : TeX().getVarDef(company),
                'TITLE' : title,}

    def add_header(self):
        return r'''%(company_header)s
        \newcommand{\tableau}{
        \begin{supertabular}{%(structure_tableau)s''' % {
        'company_header' : self.add_header_company("%s DE L'EXERCICE %s" % (
            DocTC.doc_names[self._type_doc], self._year)),
        'structure_tableau' : self.structure_tableau(), }

    def add_footer(self):
        return '\\end{supertabular}\n}'

    def add_annexe(self, ann):
        self._annexe = ann

    def annexe_definitions(self):
        self._lines.append(self.add_header_company('Annexe %s' % self._year))
        self._lines.append(TeX().getVarDef(self._annexe))

    def gen_pdf(self):
        param_gen = get_DocTC_params(self._orga, self._year, self._type_doc)
        if (self._type_doc == DocTC.BILAN) or \
            (self._type_doc == DocTC.COMPTE_RESULTAT):
            self._lines.insert(0, self.add_header())
            self._lines.append(self.add_footer())
        if (self._type_doc == DocTC.ANNEXE):
            self.annexe_definitions()
        write_pdf(param_gen, get_unicode_TeX('\n'.join(self._lines)))


class Contract:
    def __init__(self, orga, csv_file_name):
        year, month, dico_prestation = load_entries(csv_file_name)
        self._orga = orga
        self._year = year
        self._month = month
        self._client = None
        self._day_price = []
        self._dico_prestation = dico_prestation
        self._contracts = {}
        self.load()
        self.getDaysByAmendment()
        self._total_excluded_tax = None

    def __str__(self):
        return '''
_year = %(year)s
_month = %(month)s
_client = %(client)s
_day_price = %(day_price)s
_amendment = %(amendment)s
_nb_bill = %(nb_bill)s
''' % { 'year' : self._year,
        'month' : self._month,
        'client' : self._client,
        'day_price' : self._day_price,
        'amendment' : self._amendment,
        'nb_bill' : self._nb_bill }

    def getClient(self):
        CLIENT, START_TIME, STOP_TIME, AMOUNT, AMENDMENT = range(5)
        T_start = datetime.date(self._year, self._month, 1)
        T_stop = getSameDayNextMonth(T_start) + datetime.timedelta(days=int(-1))
        max_time = None
        min_time = None
        for c in sorted(self._contracts.keys()):
            row = self._contracts[c]
            TR_start = getDate(row[START_TIME])
            TR_stop = None
            if row[STOP_TIME]:
                TR_stop = getDate(row[STOP_TIME])
            if (TR_start <= T_stop and (not TR_stop or TR_stop >= T_start)) or\
                     (TR_start >= T_start and (TR_stop and TR_stop <= T_stop)):
                if not max_time or TR_start > max_time:
                    max_time = TR_start
                    self._client = row[CLIENT]
                    self._amendment = row[AMENDMENT]
                    val = [TR_start, int(row[AMOUNT])]
                    if min_time == None or TR_start < min_time:
                        self._day_price.insert(0, val)
                        min_time = TR_start
                    else:
                        self._day_price.append(val)
        if False:
            print ('self.client=%s'%self._client)
            print ('self.day_price=%s'%self._day_price)
            print ('self.amendment=%s'%self._amendment)

    def getBillNb(self):
        CLIENT, START_TIME, STOP_TIME, AMOUNT, AMENDMENT = range(5)
        min_time = None
        for c in sorted(self._contracts.keys()):
            row = self._contracts[c]
            row_start_time = getDate(row[START_TIME])
            row_stop_time = None
            if row[STOP_TIME]:
                row_stop_time = getDate(row[STOP_TIME])
            if not row[CLIENT] == self._client:
                continue
            if min_time == None or row_start_time < min_time:
                min_time = row_start_time
        self._nb_bill = 0
        if min_time:
            self._nb_bill = (self._year - min_time.year) * 12 +\
                           self._month - min_time.month + 1

    def load(self):
        CLIENT, START_TIME, STOP_TIME, AMOUNT, AMENDMENT = range(5)
        reader = get_reader(self._orga, 'contracts.csv')
        for row in reader:
            if not row or row[0] == 'client':
                continue
            self._contracts[getDate(row[START_TIME])] = row
        self.getClient()
        self.getBillNb()

    def set_nbDays(self, day_index, nb_contract):
        day = datetime.date(self._year, self._month, 1) +\
              datetime.timedelta(days=day_index)
        if nb_contract+1 < len(self._day_price):
            if day > self._day_price[nb_contract+1][0]:
                nb_contract += 1
        val = decimal.Decimal(self._dico_prestation[day_index])
        if not self._day_price:
            return 0
        if len(self._day_price[nb_contract]) == 2:
            self._day_price[nb_contract].append(val)
        else:
            self._day_price[nb_contract][2] += val
        return nb_contract

    def getDaysByAmendment(self):
        nb_contract = 0
        for week in calendar.monthcalendar(self._year, self._month):
            for d in week:
                if self._dico_prestation[d] in ('1', '0.5'):
                    nb_contract = self.set_nbDays(d, nb_contract)

    def get_calculus(self):
        sep=''
        if len(self._day_price) == 1:
            sep=' '
        return '+'.join ([
            '%s%s*%s%s' % (tjm[2],sep,sep,tjm[1]) for tjm in self._day_price])

    def get_nb_days(self):
        return sum ([ tjm[2] for tjm in self._day_price])

    def get_total_excluded_tax(self):
        if not self._total_excluded_tax:
            self._total_excluded_tax = sum (
                    [ tjm[1]*tjm[2] for tjm in self._day_price])
        return self._total_excluded_tax


    def get_VAT(self):
        if not self._total_excluded_tax:
            self._total_excluded_tax = self.get_total_excluded_tax()
        return decimal.Decimal('%.3f' % round(
            self._total_excluded_tax * decimal.Decimal(self.get_VAT_rate()), 2))

    def get_VAT_rate(self):
        if self._year<2014:
            return decimal.Decimal('0.196')
        return decimal.Decimal('0.2')

    def get_total_tax_incl(self):
        if not self._total_excluded_tax:
            self._total_excluded_tax = self.get_total_excluded_tax()
        return round(self._total_excluded_tax + self.get_VAT(),2)

    def get_dico(bill):
        return { 'year' : bill._year,
            'month name': get_month_name(bill._year, bill._month),
            'month id'  : '0'*(2-len(str(bill._month))) + str(bill._month),
            'last day'  : sorted(bill._dico_prestation.keys())[-1],
            'nb days'   : bill.get_nb_days(),
            'nb bill'   : '0'*(6-len(str(bill._nb_bill))) +str(bill._nb_bill),
            'total woVAT' : bill.get_total_excluded_tax(),
            'VAT'       : '%.2f' % bill.get_VAT(),
            'VAT rate'  : '%.2f' % (100 * bill.get_VAT_rate()),
            'total'     : '%.2f' % bill.get_total_tax_incl(),
            'calculus'  : bill.get_calculus(),
            'amendment' : bill._amendment,
        }

    def get_name(self):
        return 'bill'

def get_encoding():
    if platform.system().split('-')[0] in ('Windows', 'CYGWIN_NT'):
        return 'windows-1252'
    return 'utf-8'

class TeX:
    def __init__(self):
        pass
    def calendar(self, bill):
        tex_weeks = ''
        for week in calendar.monthcalendar(bill._year, bill._month):
            tex_weeks += '\\semaine '
            for d in week:
                tex_weeks += '{{'
                if bill._dico_prestation[d] == '0.5':
                    tex_weeks += '%s (1/2)' % str(d)
                    tex_weeks += '}{'
                    tex_weeks += '*'
                if bill._dico_prestation[d] == '1':
                    tex_weeks += str(d)
                    tex_weeks += '}{'
                    tex_weeks += '*'
                if bill._dico_prestation[d] == '0':
                    tex_weeks += str(d)
                    tex_weeks += '}{'
                    tex_weeks += '\\ '
                if bill._dico_prestation[d] == '-':
                    tex_weeks += '~'
                    tex_weeks += '}{'
                    tex_weeks += '~'
                tex_weeks += '}}'
            tex_weeks += '%\n'
        return '''\\newcommand{\\tableau}{%%\n%(tex_weeks)s\n} ''' % {
            'tex_weeks' : tex_weeks}

    def getVarDef(self, db):
        def getVarDef_fromVal(k, v):
            return r'\gdef\%s%s{%s}' % (db.get_name(),
                    ''.join([w[0].upper()+w[1:] for w in k.split()]),
                    str(v).replace('_','\_'))
        return '\n'.join([
                getVarDef_fromVal(k, v) for k,v in db.get_dico().items()])

def create_utf8_translation_table():
    tr_table = {}
    utf8_file = os.path.join(config.get_internal_data_dir(), 'utf8ienc.dtx')
    for line in open(utf8_file):
        m = re.match(r'%.*\DeclareUnicodeCharacter\{(\w+)\}\{(.*)\}', line)
        if m:
            codepoint, latex = m.groups()
            latex = latex.replace('@tabacckludge', '')
            tr_table[int(codepoint, 16)] = decode(latex)
    return tr_table

def get_unicode_TeX(tex_data):
    tr_table = create_utf8_translation_table()
    if sys.version_info[0] >= 3:
        return tex_data.translate(tr_table)
    return decode(tex_data).translate(tr_table).encode(get_encoding())


def decode(s):
    if sys.version_info[0] >= 3:
        return s
    return s.decode(get_encoding())

def get_month_name(year, month):
    month_name = datetime.date(year, month, 1).strftime('%B')
    month_name = month_name[0].upper() + month_name[1:]
    return month_name

def bill_creation(orga, bill, company):
    tex = TeX()
    db_list = [ Client(orga, bill._client), bill, company, Bank(orga)]
    return get_unicode_TeX(
        '\n'.join([tex.calendar(bill)]+[tex.getVarDef(db) for db in db_list]))

def init_bill(orga, csv_file_name):
    year, month = filename_info(csv_file_name)
    year_bill_dir = os.path.join(config.get_bills_dir(orga), str(year))
    if not os.path.exists(year_bill_dir):
        os.makedirs(year_bill_dir)
    def deco(day_of_week, day_of_month):
        if not day_of_month:
            return '-'
        if day_of_week%7 > 4:
            return '0'
        return '1'

    lines = []
    for w in calendar.monthcalendar(year, month):
        lines.append(';'.join([ deco(dw, dm) for dw, dm in enumerate(w)]) +'\n')
    csv_file_name = os.path.join(year_bill_dir, os.path.basename(csv_file_name))
    open(csv_file_name, 'a').writelines(lines)
    return csv_file_name

class Company():
    def __init__(self, orga):
        reader = get_reader(orga, 'company.csv')
        header = next_entry(reader)
        self._dico = {}
        for r in reader:
            self._dico.update(zip(header, r))
            long_form = None
            if self._dico['form'] == 'SARL':
                long_form = 'Société à Responsabilité Limitée'
            VAT_intra = self._dico['VAT code prefix'] + self._dico['Siren'].strip()
            capital = locale.format('%d', int(self._dico['capital']),
                    grouping=True)
            self._dico.update({
                'intracommunautary VAT' : VAT_intra,
                'compact siren' : ''.join(self._dico['Siren'].split()),
                'capital' : capital, 'Company long form' : long_form, })
            break; #We select just the first company name

    def get_name(self):
        return 'company'

    def get_dico(self):
        return self._dico

    def __getitem__(self, k):
        return self._dico[k]

class Bank():
    def __init__(self, orga):
        reader = get_reader(orga, 'bank_accounts.csv')
        header = next_entry(reader)
        self._dico = {}
        for r in reader:
            self._dico.update(zip(header, r))
            iban = ''.join(self._dico[h] for h in [
                    'code', 'agency', 'account number', 'key'])
            # print ('iban=%s' % iban)
            IBAN = ' '.join( [ iban[4*i:4*(i+1)]
                        for i in range(len(iban)//4 + len(iban)%4)])
            # print ('IBAN=%s' % IBAN)
            self._dico.update({ 'IBAN' : IBAN,
                    'short account number' : self._dico['account number']})
            break; #We select just the first bank

    def get_name(self):
        return 'bank'

    def get_dico(self):
        return self._dico

    def __getitem__(self, k):
        return self._dico[k]

class Client():
    def __init__(self, orga, client_name):
        reader = get_reader(orga, 'clients.csv')
        header = next_entry(reader)
        client_info = []
        for row in reader:
            if row[0] == client_name:
                client_info = row
                break
        if not client_info:
            sys.stderr.write(_('Client {0} not found in {1}\n').format(
                        client_name, 'clients.csv'))
            sys.exit(2)
        self._dico = {}
        self._dico.update(zip(header, client_info))

    def get_name(self):
        return 'client'

    def get_dico(self):
        return self._dico

def main(orga, csv_file_name):
    root_dir = config.get_value('root', orga)
    if not os.path.exists(root_dir):
        sys.stderr.write(_(
            'config root:"%s" no such directory, please check!\n') % root_dir)
        return 2

    if not os.path.isfile(csv_file_name):
        csv_file_name = init_bill(orga, csv_file_name)

    bill = Contract(orga, csv_file_name)
    company = Company(orga)
    tex_data = bill_creation(orga, bill, company)
    dico_bill = get_bill_params(orga, bill._year, bill._month, company['Name'])
    write_pdf(dico_bill, tex_data)

if __name__ == '__main__':
    args = config.get_args(bill_name=True)
    sys.exit(main(args.orga, args.bill_name))
