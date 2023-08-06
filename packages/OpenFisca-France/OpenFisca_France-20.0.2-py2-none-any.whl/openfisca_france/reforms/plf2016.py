# -*- coding: utf-8 -*-


from __future__ import division

import os

from ..model.base import *


dir_path = os.path.join(os.path.dirname(__file__), 'parameters')


# What if the reform was applied the year before it should

def reform_modify_parameters(parameters):
    file_path = os.path.join(dir_path, 'plf2016.yaml')
    reform_parameters_subtree = load_parameter_file(name='plf2016', file_path=file_path)
    parameters.add_child('plf2016', reform_parameters_subtree)
    return parameters


class plf2016(Reform):
    name = u'Projet de Loi de Finances 2016 appliquée aux revenus 2014'
    # key = 'plf2016'

    class decote(Variable):
        label = u"Décote IR 2016 appliquée en 2015 sur revenus 2014"
        definition_period = YEAR

        # This formula is copy-pasted from the reference decote formula, so that we only change the decote formula for 2014
        def formula_2015_01_01(self, simulation, period):
            ir_plaf_qf = simulation.calculate('ir_plaf_qf', period)
            nb_adult = simulation.calculate('nb_adult', period)
            decote_seuil_celib = simulation.parameters_at(period.start).impot_revenu.decote.seuil_celib
            decote_seuil_couple = simulation.parameters_at(period.start).impot_revenu.decote.seuil_couple
            decote_celib = (ir_plaf_qf < 4 / 3 * decote_seuil_celib) * (decote_seuil_celib - 3 / 4 * ir_plaf_qf)
            decote_couple = (ir_plaf_qf < 4 / 3 * decote_seuil_couple) * (decote_seuil_couple - 3 / 4 * ir_plaf_qf)

            return (nb_adult == 1) * decote_celib + (nb_adult == 2) * decote_couple

        def formula_2014_01_01(self, simulation, period):
            ir_plaf_qf = simulation.calculate('ir_plaf_qf', period)
            nb_adult = simulation.calculate('nb_adult', period)
            plf = simulation.parameters_at(period.start).plf2016

            decote_celib = (ir_plaf_qf < plf.decote_seuil_celib) * (plf.decote_seuil_celib - .75 * ir_plaf_qf)
            decote_couple = (ir_plaf_qf < plf.decote_seuil_couple) * (plf.decote_seuil_couple - .75 * ir_plaf_qf)
            return (nb_adult == 1) * decote_celib + (nb_adult == 2) * decote_couple

    def apply(self):
        self.update_variable(self.decote)
        self.modify_parameters(modifier_function = reform_modify_parameters)


# Counterfactual ie business as usual

def counterfactual_modify_parameters(parameters):
    # TODO: inflater les paramètres de la décote le barème de l'IR
    inflation = .001
    reform_parameters_subtree = ParameterNode('plf2016_conterfactual', data = {
        'decote_seuil_celib': {'values': {"2015-01-01": {'value': round(1135 * (1 + inflation))}, "2016-01-01": {'value': None}}},
        'decote_seuil_couple': {'values': {"2015-01-01": {'value': round(1870 * (1 + inflation))}, "2065-01-01": {'value': None}}},
        })
    parameters.add_child('plf2016_conterfactual', reform_parameters_subtree)
    return parameters

    # WIP : Nouveaux parametres à actualiser :
    # 1° Le 1 est remplacé par les dispositions suivantes :
    # (3) « 1. L'impôt est calculé en appliquant à la fraction de chaque part de revenu qui excède 9 700 € le taux de :
    # (4) « 14 % pour la fraction supérieure à 9 700 € et inférieure ou égale à 26 791 € ;
    # (5) « 30 % pour la fraction supérieure à 26 791 € et inférieure ou égale à 71 826 € ;
    # (6) « 41 % pour la fraction supérieure à 71 826 € et inférieure ou égale à 152 108 € ;
    # (7) « 45 % pour la fraction supérieure à 152 108 €. » ;
    # (8) 2° Au 2 :
    # (9) a) Au premier alinéa, le montant : « 1 508 € » est remplacé par le montant : « 1 510 € » ;
    # (10) b) Au deuxième alinéa, le montant : « 3 558 € » est remplacé par le montant : « 3 562 € » ;
    # (11) c) Au troisième alinéa, le montant : « 901 € » est remplacé par le montant : « 902 € » ;
    # (12) d) Au quatrième alinéa, le montant : « 1 504 € » est remplacé par le montant : « 1 506 € » ;
    # (13) e) Au dernier alinéa, le montant : « 1 680 € » est remplacé par le montant : « 1 682 € » ;
    # (14) 3° Au 4, les mots : « 1 135 € et » sont remplacés par les mots : « 1 165 € et les trois quarts de » et
    # les mots : « 1 870 €
    # et » sont remplacés par les mots : « 1 920 € et les trois quarts de ».
    # (15) II. – Au second alinéa de l'article 196 B du même code, le montant : « 5 726 € » est remplacé par le
    # montant : « 5 732 € ».


class plf2016_counterfactual(Reform):
    name = u'Contrefactuel du PLF 2016 sur les revenus 2015'
    # key = 'plf2016_counterfactual'

    class decote(Variable):
        label = u"Décote IR 2015 appliquée sur revenus 2015 (contrefactuel)"
        definition_period = YEAR

        def formula_2015_01_01(self, simulation, period):
            ir_plaf_qf = simulation.calculate('ir_plaf_qf', period)
            inflator = 1 + .001 + .005
            decote = simulation.parameters_at(period.start).impot_revenu.decote
            assert decote.seuil == 1016
            return (ir_plaf_qf < decote.seuil * inflator) * (decote.seuil * inflator - ir_plaf_qf) * 0.5

    class reduction_impot_exceptionnelle(Variable):
        end = ''

        def formula_2015_01_01(self, simulation, period):
            nb_adult = simulation.calculate('nb_adult', period)
            nb_parents = simulation.calculate('nb_parents', period.first_month)
            rfr = simulation.calculate('rfr', period)
            inflator = 1 + .001 + .005
            # params = simulation.parameters_at(period.start).impot_revenu.reductions_impots.reduction_impot_exceptionnelle
            seuil = 13795 * inflator
            majoration_seuil = 3536 * inflator
            montant_plafond = 350 * inflator
            plafond = seuil * nb_adult + (nb_parents - nb_adult) * 2 * majoration_seuil
            montant = montant_plafond * nb_adult
            return min_(max_(plafond + montant - rfr, 0), montant)

    class reductions(Variable):
        label = u"Somme des réductions d'impôt"
        definition_period = YEAR

        def formula_2013_01_01(self, simulation, period):
            accult = simulation.calculate('accult', period)
            adhcga = simulation.calculate('adhcga', period)
            cappme = simulation.calculate('cappme', period)
            creaen = simulation.calculate('creaen', period)
            daepad = simulation.calculate('daepad', period)
            deffor = simulation.calculate('deffor', period)
            dfppce = simulation.calculate('dfppce', period)
            doment = simulation.calculate('doment', period)
            domlog = simulation.calculate('domlog', period)
            donapd = simulation.calculate('donapd', period)
            duflot = simulation.calculate('duflot', period)
            ecpess = simulation.calculate('ecpess', period)
            garext = simulation.calculate('garext', period)
            intagr = simulation.calculate('intagr', period)
            invfor = simulation.calculate('invfor', period)
            invlst = simulation.calculate('invlst', period)
            ip_net = simulation.calculate('ip_net', period)
            locmeu = simulation.calculate('locmeu', period)
            mecena = simulation.calculate('mecena', period)
            mohist = simulation.calculate('mohist', period)
            patnat = simulation.calculate('patnat', period)
            prcomp = simulation.calculate('prcomp', period)
            reduction_impot_exceptionnelle = simulation.calculate('reduction_impot_exceptionnelle', period)
            repsoc = simulation.calculate('repsoc', period)
            resimm = simulation.calculate('resimm', period)
            rsceha = simulation.calculate('rsceha', period)
            saldom = simulation.calculate('saldom', period)
            scelli = simulation.calculate('scelli', period)
            sofica = simulation.calculate('sofica', period)
            spfcpi = simulation.calculate('spfcpi', period)
            total_reductions = accult + adhcga + cappme + creaen + daepad + deffor + dfppce + doment + domlog + \
                donapd + duflot + ecpess + garext + intagr + invfor + invlst + locmeu + mecena + mohist + patnat + \
                prcomp + repsoc + resimm + rsceha + saldom + scelli + sofica + spfcpi + reduction_impot_exceptionnelle

            return min_(ip_net, total_reductions)

    def apply(self):
        for variable in [self.decote, self.reductions, self.reduction_impot_exceptionnelle]:
            self.update_variable(variable)
        self.modify_parameters(modifier_function = counterfactual_modify_parameters)


def counterfactual_2014_modify_parameters(parameters):
    # TODO: inflater les paramètres de la décote le barème de l'IR
    inflator = 1 + .001 + .005
    reform_year = 2015
    reform_period = period(reform_year)
    # parameters.ir.reductions_impots.reduction_impot_exceptionnelle.montant_plafond.update(period=reform_period, value=350*inflator)
    # parameters.ir.reductions_impots.reduction_impot_exceptionnelle.seuil.update(period=reform_period, value=13795*inflator)
    # parameters.ir.reductions_impots.reduction_impot_exceptionnelle.majoration_seuil.update(period=reform_period, value=3536*inflator)
    parameters.impot_revenu.bareme[1].threshold.update(period=reform_period, value=6011*inflator)
    parameters.impot_revenu.bareme[1].rate.update(period=reform_period, value=.055*inflator)
    parameters.impot_revenu.bareme[2].threshold.update(period=reform_period, value=11991*inflator)
    parameters.impot_revenu.bareme[2].rate.update(period=reform_period, value=.14*inflator)
    parameters.impot_revenu.bareme[3].threshold.update(period=reform_period, value=26631*inflator)
    parameters.impot_revenu.bareme[3].rate.update(period=reform_period, value=.30*inflator)
    parameters.impot_revenu.bareme[4].threshold.update(period=reform_period, value=71397*inflator)
    parameters.impot_revenu.bareme[4].rate.update(period=reform_period, value=.40*inflator)

    return parameters


class plf2016_counterfactual_2014(Reform):
    name = u'Contrefactuel 2014 du PLF 2016 sur les revenus 2015'
    key = 'plf2016_counterfactual_2014'

    class decote(Variable):
        definition_period = YEAR

        def formula_2015_01_01(self, simulation, period):
            ir_plaf_qf = simulation.calculate('ir_plaf_qf', period)
            inflator = 1 + .001 + .005
            decote = simulation.parameters_at(period.start).impot_revenu.decote
            assert decote.seuil == 1016
            return (ir_plaf_qf < decote.seuil * inflator) * (decote.seuil * inflator - ir_plaf_qf) * 0.5

    class reduction_impot_exceptionnelle(Variable):
        end = ''

        def formula_2015_01_01(self, simulation, period):
            nb_adult = simulation.calculate('nb_adult', period)
            nb_parents = simulation.calculate('nb_parents', period.first_month)
            rfr = simulation.calculate('rfr', period)
            inflator = 1 + .001 + .005
            # params = simulation.parameters_at(period.start).impot_revenu.reductions_impots.reduction_impot_exceptionnelle
            seuil = 13795 * inflator
            majoration_seuil = 3536 * inflator
            montant_plafond = 350 * inflator
            plafond = seuil * nb_adult + (nb_parents - nb_adult) * 2 * majoration_seuil
            montant = montant_plafond * nb_adult
            return min_(max_(plafond + montant - rfr, 0), montant)

    class reductions(Variable):
        label = u"Somme des réductions d'impôt"
        definition_period = YEAR

        def formula_2013_01_01(self, simulation, period):
            accult = simulation.calculate('accult', period)
            adhcga = simulation.calculate('adhcga', period)
            cappme = simulation.calculate('cappme', period)
            creaen = simulation.calculate('creaen', period)
            daepad = simulation.calculate('daepad', period)
            deffor = simulation.calculate('deffor', period)
            dfppce = simulation.calculate('dfppce', period)
            doment = simulation.calculate('doment', period)
            domlog = simulation.calculate('domlog', period)
            donapd = simulation.calculate('donapd', period)
            duflot = simulation.calculate('duflot', period)
            ecpess = simulation.calculate('ecpess', period)
            garext = simulation.calculate('garext', period)
            intagr = simulation.calculate('intagr', period)
            invfor = simulation.calculate('invfor', period)
            invlst = simulation.calculate('invlst', period)
            ip_net = simulation.calculate('ip_net', period)
            locmeu = simulation.calculate('locmeu', period)
            mecena = simulation.calculate('mecena', period)
            mohist = simulation.calculate('mohist', period)
            patnat = simulation.calculate('patnat', period)
            prcomp = simulation.calculate('prcomp', period)
            reduction_impot_exceptionnelle = simulation.calculate('reduction_impot_exceptionnelle', period)
            repsoc = simulation.calculate('repsoc', period)
            resimm = simulation.calculate('resimm', period)
            rsceha = simulation.calculate('rsceha', period)
            saldom = simulation.calculate('saldom', period)
            scelli = simulation.calculate('scelli', period)
            sofica = simulation.calculate('sofica', period)
            spfcpi = simulation.calculate('spfcpi', period)
            total_reductions = accult + adhcga + cappme + creaen + daepad + deffor + dfppce + doment + domlog + \
                donapd + duflot + ecpess + garext + intagr + invfor + invlst + locmeu + mecena + mohist + patnat + \
                prcomp + repsoc + resimm + rsceha + saldom + scelli + sofica + spfcpi + reduction_impot_exceptionnelle

            return min_(ip_net, total_reductions)

    def apply(self):
        for variable in [self.decote, self.reduction_impot_exceptionnelle, self.reductions]:
            self.update_variable(variable)
        self.modify_parameters(modifier_function = counterfactual_2014_modify_parameters)
