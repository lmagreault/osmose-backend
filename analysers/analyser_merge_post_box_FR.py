#!/usr/bin/env python
#-*- coding: utf-8 -*-

###########################################################################
##                                                                       ##
## Copyrights Frédéric Rodrigo 2015-2016                                 ##
##                                                                       ##
## This program is free software: you can redistribute it and/or modify  ##
## it under the terms of the GNU General Public License as published by  ##
## the Free Software Foundation, either version 3 of the License, or     ##
## (at your option) any later version.                                   ##
##                                                                       ##
## This program is distributed in the hope that it will be useful,       ##
## but WITHOUT ANY WARRANTY; without even the implied warranty of        ##
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         ##
## GNU General Public License for more details.                          ##
##                                                                       ##
## You should have received a copy of the GNU General Public License     ##
## along with this program.  If not, see <http://www.gnu.org/licenses/>. ##
##                                                                       ##
###########################################################################

from modules.OsmoseTranslation import T_
from .Analyser_Merge import Analyser_Merge, SourceOpenDataSoft, CSV, Load, Conflate, Select, Mapping


class Analyser_Merge_Post_box_FR(Analyser_Merge):
    def __init__(self, config, logger = None):
        Analyser_Merge.__init__(self, config, logger)
        self.def_class_missing_official(item = 8025, id = 1, level = 3, tags = ['merge', 'post', 'fix:survey', 'fix:picture'],
            title = T_('Post box not integrated'))
        self.def_class_missing_osm(item = 7051, id = 2, level = 3, tags = ['merge', 'post', 'fix:chair'],
            title = T_('Post box without tag "ref" or invalid'))
        self.def_class_possible_merge(item = 8026, id = 3, level = 3, tags = ['merge', 'post', 'fix:chair'],
            title = T_('Post box, integration suggestion'))

        self.init(
            "https://datanova.legroupe.laposte.fr/explore/dataset/laposte_boiterue",
            "Liste des boîtes aux lettres de rue France métropolitaine et DOM",
            CSV(SourceOpenDataSoft(
                attribution = "data.gouv.fr:LaPoste",
                url="https://datanova.legroupe.laposte.fr/explore/dataset/laposte_boiterue")),
            Load("Latlong", "Latlong",
                xFunction = lambda x: x and x.split(',')[1],
                yFunction = lambda y: y and y.split(',')[0]),
            Conflate(
                select = Select(
                    types = ["nodes"],
                    tags = {"amenity": "post_box"}),
                osmRef = "ref",
                conflationDistance = 50,
                missing_official_fix = False,
                mapping = Mapping(
                    static1 = {
                        "amenity": "post_box",
                        "operator": "La Poste"},
                    static2 = {"source": self.source},
                    mapping1 = {"ref": "CO_MUP"},
                text = lambda tags, fields: {"en": ", ".join(filter(lambda x: x, [fields["VA_NO_VOIE"], fields["LB_EXTENSION"].strip(), fields["LB_VOIE_EXT"], fields["CO_POSTAL"], fields["LB_COM"]]))} )))
