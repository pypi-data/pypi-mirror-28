# -*- coding: utf-8 -*-

from __future__ import division

from openfisca_core.reforms import Reform
from numpy import vectorize, logical_or as or_, absolute as abs_

from ..model.base import *


class perte_autonomie(Variable):
    value_type = bool
    entity = Individu
    label = u"Personne en perte d'autonomie"

class resident_93(Variable):
    value_type = bool
    label = u"Résident en Seine-Saint-Denis"
    entity = Menage

    def formula(self, simulation, period):
        period = period.first_month
        depcom = simulation.calculate('depcom', period)

        def is_resident_93(code_insee):
            prefix = code_insee[0:2]
            result = (prefix == "93")
            return result

        is_resident_93_vec = vectorize(is_resident_93)

        result = is_resident_93_vec(depcom)

        return result

class adpa_eligibilite(Variable):
    value_type = bool
    label = u"Eligibilité à l'ADPA"
    entity = Individu

    def formula(self, simulation, period):
        period = period.first_month
        age = simulation.calculate('age', period)
        resident_93 = simulation.calculate('resident_93', period)
        perte_autonomie = simulation.calculate('perte_autonomie', period)

        result = (age >= 60) * resident_93 * perte_autonomie

        return result

class adpa_base_ressources_i(Variable):
    value_type = float
    label = u"Base ressources ADPA pour un individu"
    entity = Individu

    def formula(self, simulation, period):
        period = period.first_month
        previous_year = period.start.period('year').offset(-1)
        salaire_imposable = simulation.calculate_add('salaire_imposable', period.n_2)
        retraite_imposable = simulation.calculate_add('retraite_imposable', period.n_2)
        chomage_imposable = simulation.calculate_add('chomage_imposable', period.n_2)
        revenus_capital = simulation.calculate_add('revenus_capital', previous_year)
        revenus_locatifs = simulation.calculate_add('revenus_locatifs', previous_year, options = [ADD])
        # Prélevements libératoire forfaitaire à prendre en compte sans abattement
        valeur_locative_immo_non_loue = simulation.calculate_add('valeur_locative_immo_non_loue', previous_year)
        valeur_locative_terrains_non_loue = simulation.calculate_add('valeur_locative_terrains_non_loue', previous_year)

        base_ressource_mensuelle = (
            salaire_imposable + retraite_imposable + chomage_imposable + revenus_locatifs +
            revenus_capital * 0.30 +
            valeur_locative_immo_non_loue * 0.5 +
            valeur_locative_terrains_non_loue * 0.8
        ) / 12

        return base_ressource_mensuelle

class adpa_base_ressources(Variable):
    value_type = float
    label = u"Base ressources ADPA pour une famille"
    entity = Famille

    def formula(self, simulation, period):
        period = period.first_month
        adpa_base_ressources_i = simulation.compute('adpa_base_ressources_i', period)
        adpa_base_ressources = self.sum_by_entity(adpa_base_ressources_i)

        return adpa_base_ressources

class adpa(Variable):
    value_type = float
    label = u"ADPA"
    entity = Famille

    def formula(self, simulation, period):
        period = period.first_month

        adpa_eligibilite_holder = simulation.compute('adpa_eligibilite', period)
        adpa_eligibilite = self.any_by_roles(adpa_eligibilite_holder)
        base_ressource_mensuelle = simulation.calculate('adpa_base_ressources', period)
        en_couple = simulation.calculate('en_couple', period)

        # On ne prend pas en compte le cas où le conjoint est placé.
        quotient_familial = 1 + 0.7 * en_couple
        base_ressource_mensuelle = base_ressource_mensuelle / quotient_familial

        majorationTiercePersonne = 1103.08
        seuil1 = 0.67 * majorationTiercePersonne
        seuil2 = 2.67 * majorationTiercePersonne

        participation_usager = (
            (base_ressource_mensuelle < seuil1) * 0 +
            (base_ressource_mensuelle >= seuil1) * (base_ressource_mensuelle <= seuil2) *
                 90 * (base_ressource_mensuelle - seuil1) / (2 * majorationTiercePersonne) +
            (base_ressource_mensuelle > seuil2) * 90
        )

        participation_departement = 100 - participation_usager

        return participation_departement * adpa_eligibilite


class aides_cd93(Reform):
    name = u'Aides du conseil départemental du 93'

    def apply(self):
        self.add_variables(perte_autonomie, resident_93, adpa_eligibilite, adpa_base_ressources_i, adpa_base_ressources, adpa)
