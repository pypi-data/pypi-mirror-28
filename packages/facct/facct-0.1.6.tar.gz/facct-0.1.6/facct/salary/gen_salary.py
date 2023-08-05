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
import facct.config as config
from facct.i18n import _
import decimal

def filename_info(csv_file_name):
    base_name = os.path.basename(csv_file_name).split('.')[0]
    if len(base_name)<4:
        sys.stderr.write(_('No correct input file name (eg. 2011.csv)\n'))
        sys.exit(2)
    year = int(base_name)
    return year

def next_entry(reader):
    for r in reader: return r
    return []

def get_salaries(orga, csv_file_name):
    reader = csv.reader(open(csv_file_name, 'r'), delimiter=';', quotechar='"')
    salaries = []
    year = filename_info(csv_file_name)
    while True:
        r = next_entry(reader)
        if not r: break
        salaries.append(Salary(orga, year, int(r[0]), decimal.Decimal(r[1])))
    return salaries


class Salary:
    wages_total = 0
    nb_month = 0
    epsilon = decimal.Decimal('.01')
    debug = False
    def __init__(self, orga, year, month, wage):
        self._orga = orga
        self._year = year
        self._month = month
        self._wage = wage
        Salary.wages_total += wage
        Salary.nb_month += 1

    def get_wages(self):
        return self._wage

    def get_month_charge(self, val):
        return decimal.Decimal(val)/Salary.nb_month

    def get_indem_jour(self):
        rate = decimal.Decimal(0.007)
        tot = min(Salary.wages_total, 196140) * rate
        return self.get_month_charge(tot)

    def get_maladie(self):
        rate_min = decimal.Decimal(0.03)
        rate_2 = decimal.Decimal(0.065)
        seuil_1 = decimal.Decimal(27459.60)
        part_1 = min(seuil_1, Salary.wages_total)
        rate_1 = (part_1 * (rate_2 - rate_min) / seuil_1) + rate_min

        tot = part_1 * rate_1
        if Salary.wages_total > seuil_1:
            tot += (Salary.wages_total - seuil_1) * rate_2
        return self.get_month_charge(tot)

    def get_rsi(self):
        # https://www.rsi.fr/cotisations/artisans-commercants/
        #    calcul-des-cotisations/taux-de-cotisations.html
        maladie = self.get_maladie()
        indem_jour = self.get_indem_jour()
        rsi = decimal.Decimal(maladie + indem_jour).quantize(
                Salary.epsilon)
        if Salary.debug:
            print ('rsi=%s' % rsi)
        return rsi

    def get_formation_pro(self):
        plafond_secu = decimal.Decimal(38616)
        rate_1 = decimal.Decimal(0.0025)
        return self.get_month_charge (plafond_secu * rate_1)

    def get_csg_crds(self):
        rate_1 = decimal.Decimal(0.08)
        return self.get_month_charge(Salary.wages_total * rate_1)

    def get_alloc_f(self):
        seuil_1 = decimal.Decimal(43151)
        rate_1 = decimal.Decimal(0.0215)
        rate_3 = decimal.Decimal(0.0525)
        seuil_2 = decimal.Decimal(54919)

        tot = Salary.wages_total * rate_1
        if Salary.wages_total < seuil_1:
            return self.get_month_charge(tot)

        part_2 = min(seuil_2, Salary.wages_total) - seuil_1
        rate_2 = (part_2 * (rate_3-rate_1)/ (seuil_2 - seuil_1)) + rate_1
        tot += part_2 * rate_2
        if Salary.wages_total < seuil_2:
            return self.get_month_charge(tot)

        part_3 = Salary.wages_total - seuil_2
        tot += part_3 * rate_3
        return self.get_month_charge(tot)

    def get_urssaf(self):
        # https://www.urssaf.fr/portail/home/taux-et-baremes/
        #  taux-de-cotisations/les-professions-liberales/
        #  bases-de-calcul-et-taux-des-coti.html
        alloc_familliales = self.get_alloc_f()
        formation_pro = self.get_formation_pro()
        csg_crds = self.get_csg_crds()
        urssaf = decimal.Decimal(
                formation_pro + alloc_familliales + csg_crds).quantize(
                Salary.epsilon)
        if Salary.debug:
            print ('alloc_familliales=%s' % alloc_familliales)
            print ('formation_pro=%s' % formation_pro)
            print ('csg_crds=%s' % csg_crds)
            print ('urssaf=%s' % urssaf)
        return urssaf

    def get_retraite_comp(self):

        tab = [ (0, 1277),
                (26581, 2553),
                (49281, 3830),
                (57851, 6384),
                (66401, 8937),
                (83061, 14044),
                (103181, 15320),
                (123301, 16597), ]
        tot = 0
        for slot in tab:
            if Salary.wages_total > slot[0]:
                tot = slot[1]
            else:
                break
        return self.get_month_charge(tot)

    def get_retraite_base(self):
        seuil_1 = decimal.Decimal(4511)
        rate_1 = decimal.Decimal(0.0823)
        seuil_2 = decimal.Decimal(39228)
        rate_2 = decimal.Decimal(0.0187)
        seuil_3 = decimal.Decimal(196140)

        tot = decimal.Decimal(455)
        if Salary.wages_total < seuil_1:
            return self.get_month_charge(tot)

        part_2 = min(Salary.wages_total, seuil_2) - seuil_1
        tot += part_2 * rate_1
        if Salary.wages_total < seuil_2:
            return self.get_month_charge(tot)

        part_3 = min(Salary.wages_total, seuil_3) - seuil_2
        tot += part_3 * rate_2
        return self.get_month_charge(tot)

    def get_inval_dece(self):
        # Class A
        return self.get_month_charge(76)

    def get_cipav(self):
        # https://www.lacipav.fr/sites/default/files/2017-03/
        #  FP%20calcul%20cotisation.2017.2.pdf
        # https://www.lecoindesentrepreneurs.fr/
        #  affiliation-et-cotisations-a-la-cipav/
        retraite_base = self.get_retraite_base()
        retraite_comp = self.get_retraite_comp()
        inval_dece = self.get_inval_dece()
        cipav = decimal.Decimal (
                retraite_base + retraite_comp + inval_dece).quantize(
                Salary.epsilon)
        if Salary.debug:
            print ('retraite_base=%s' % retraite_base)
            print ('retraite_comp=%s' % retraite_comp)
            print ('inval_dece=%s' % inval_dece)
            print ('cipav=%s' % cipav)
        return cipav

if __name__ == '__main__':
    args = config.get_args(salary_name=True)
    sys.exit(main(args.orga, args.salary_name))

