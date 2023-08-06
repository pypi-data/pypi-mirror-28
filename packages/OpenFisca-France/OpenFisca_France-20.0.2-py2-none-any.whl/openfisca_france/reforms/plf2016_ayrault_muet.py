# -*- coding: utf-8 -*-

from __future__ import division

import os

from ..model.base import *


dir_path = os.path.dirname(__file__)


# Réforme de l'amendement Ayrault-Muet

def ayrault_muet_modify_parameters(parameters):
    # TODO: inflater les paramètres de la décote le barème de l'IR
    inflator = 1
    for inflation in [2.8, 0.1, 1.5, 2.1, 2, 0.9, 0.5, 0.1]:
        inflator = inflator * (1 + inflation / 100)
    del inflation

    elig1 = Parameter('elig1', {'values': {"2015-01-01": {'value': round(16251 * inflator)}, "2016-01-01": {'value': None}}})
    elig2 = Parameter('elig2', {'values': {"2015-01-01": {'value': round(32498 * inflator)}, "2016-01-01": {'value': None}}})
    elig3 = Parameter('elig3', {'values': {"2015-01-01": {'value': round(4490 * inflator)}, "2016-01-01": {'value': None}}})
    parameters.impot_revenu.credits_impot.ppe.add_child('elig1', elig1)
    parameters.impot_revenu.credits_impot.ppe.add_child('elig2', elig2)
    parameters.impot_revenu.credits_impot.ppe.add_child('elig3', elig3)
    return parameters


class variator(Variable):
    value_type = float
    default_value = 1
    entity = FoyerFiscal
    label = u'Multiplicateur du seuil de régularisation'
    definition_period = YEAR


class reduction_csg(Variable):
    value_type = float
    entity = Individu
    label = u"Réduction dégressive de CSG"
    definition_period = YEAR

    def formula_2015_01_01(self, simulation, period):
        smic_proratise = simulation.calculate_add('smic_proratise', period)
        assiette_csg_abattue = simulation.calculate_add('assiette_csg_abattue', period)

        seuil = 1.34
        coefficient_correctif = .9
        taux_csg = (
            simulation.parameters_at(period.start).csg.activite.imposable.taux +
            simulation.parameters_at(period.start).csg.activite.deductible.taux
            )
        tx_max = coefficient_correctif * taux_csg
        ratio_smic_salaire = smic_proratise / (assiette_csg_abattue + 1e-16)
        # règle d'arrondi: 4 décimales au dix-millième le plus proche
        taux_allegement_csg = tx_max * min_(1, max_(seuil - 1 / ratio_smic_salaire, 0) / (seuil - 1))
        # Montant de l'allegment
        return taux_allegement_csg * assiette_csg_abattue


class reduction_csg_foyer_fiscal(Variable):
    entity = FoyerFiscal
    label = u"Réduction dégressive de CSG des memebres du foyer fiscal"
    value_type = float
    definition_period = YEAR

    def formula(self, simulation, period):
        reduction_csg = simulation.calculate('reduction_csg', period)
        return simulation.foyer_fiscal.sum(reduction_csg)


class reduction_csg_nette(Variable):
    value_type = float
    entity = Individu
    label = u"Réduction dégressive de CSG"
    definition_period = YEAR

    def formula_2015_01_01(individu, period):
        reduction_csg = individu('reduction_csg', period)
        ppe_elig_bis = individu.foyer_fiscal('ppe_elig_bis', period)
        return reduction_csg * ppe_elig_bis


class ppe_elig_bis(Variable):
    value_type = bool
    entity = FoyerFiscal
    label = u"ppe_elig_bis"
    definition_period = YEAR

    def formula(self, simulation, period):
        '''
        PPE: eligibilité à la ppe, condition sur le revenu fiscal de référence
        'foy'
        '''
        rfr = simulation.calculate('rfr', period)
        ppe_coef = simulation.calculate('ppe_coef', period)
        maries_ou_pacses = simulation.calculate('maries_ou_pacses', period)
        veuf = simulation.calculate('veuf', period)
        celibataire_ou_divorce = simulation.calculate('celibataire_ou_divorce', period)
        nbptr = simulation.calculate('nbptr', period)
        variator = simulation.calculate('variator', period)
        ppe = simulation.parameters_at(period.start).impot_revenu.credits_impot.ppe
        seuil = (veuf | celibataire_ou_divorce) * (ppe.eligi1 + 2 * max_(nbptr - 1, 0) * ppe.eligi3) \
            + maries_ou_pacses * (ppe.eligi2 + 2 * max_(nbptr - 2, 0) * ppe.eligi3)
        return (rfr * ppe_coef) <= (seuil * variator)


class regularisation_reduction_csg(Variable):
    value_type = float
    entity = FoyerFiscal
    label = u"Régularisation complète réduction dégressive de CSG"
    definition_period = YEAR

    def formula_2015_01_01(self, simulation, period):
        reduction_csg = simulation.calculate('reduction_csg_foyer_fiscal', period)
        ppe_elig_bis = simulation.calculate('ppe_elig_bis', period)
        return not_(ppe_elig_bis) * (reduction_csg > 1)


class ayrault_muet(Reform):
    name = u'Amendement Ayrault-Muet au PLF2016'
    key = 'ayrault_muet'

    def apply(self):
        for variable in [
            reduction_csg,
            regularisation_reduction_csg,
            reduction_csg_foyer_fiscal,
            reduction_csg_nette,
            ppe_elig_bis,
            variator,
            ]:
            self.update_variable(variable)
        self.modify_parameters(modifier_function = ayrault_muet_modify_parameters)
