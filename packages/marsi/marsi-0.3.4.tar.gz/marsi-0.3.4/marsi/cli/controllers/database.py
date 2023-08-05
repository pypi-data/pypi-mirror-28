# Copyright 2017 Chr. Hansen A/S and The Novo Nordisk Foundation Center for Biosustainability, DTU.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

# http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from __future__ import with_statement

import os
import tempfile

import pubchempy
from IProgress import ProgressBar, Bar, ETA
from alembic import command
from alembic.config import Config
from bioservices import ChEBI
from cement.core.controller import CementBaseController, expose
from pandas import read_excel

from marsi.chemistry import openbabel
from marsi.config import db_url
from marsi.io.build_database import build_database
from marsi.io.db import Reference, Synonym, Metabolite
from marsi.io.enrichment import find_best_chebi_structure
from marsi.io.parsers import parse_chebi_data, parse_pubchem, parse_kegg_brite
from marsi.io.retriaval import retrieve_chebi_names, retrieve_chebi_relation, retrieve_chebi_vertice, \
    retrieve_chebi_structures, retrieve_drugbank_open_structures, retrieve_drugbank_open_vocabulary, \
    retrieve_bigg_reactions, retrieve_bigg_metabolites, retrieve_kegg_brite, retrieve_pubchem_mol_files, \
    retrieve_kegg_mol_files, retrieve_zinc_structures
from marsi.utils import data_dir, src_dir, internal_data_dir


PUBCHEM_COMPOUND = "PubChem Compound"
CHEBI = "ChEBI"


class DatabaseController(CementBaseController):
    # TODO: migrate database
    class Meta:
        label = 'db'
        stacked_on = 'base'
        stacked_type = 'nested'
        description = "Initialise MARSI (download data and build initial database)"
        arguments = [
            (['--drugbank-version'], dict(help="DrugBank version (5.0.3)")),
            (['--with-zinc'], dict(help="Include Zinc", action="store_true"))
        ]

    @expose(hide=True)
    def default(self):
        print("MARSI database commands. If it is the first time run 'marsi db init' For details run marsi init --help")

    @expose(hide=False, help="Build and populate database")
    def init(self):
        self.migrate()
        self.download()
        self.build_data()
        self.build_database()

    @expose(hide=True)
    def migrate(self):
        """
        Run database migration.
        """
        alembic_cfg = Config(os.path.join(src_dir, "alembic.ini"))
        alembic_cfg.set_section_option("alembic", "sqlalchemy.url", db_url)
        script_location = alembic_cfg.get_section_option("alembic", "script_location")
        alembic_cfg.set_section_option("alembic", "script_location", os.path.join(src_dir, script_location))
        command.upgrade(alembic_cfg, "head")

    @expose(hide=False, help="Download all files")
    def download(self):
        self.download_chebi()
        self.download_drug_bank()
        self.download_kegg()
        self.download_pubchem()
        self.download_bigg()
        if self.app.pargs.with_zinc:
            self.download_zinc()

    @expose(help="Retrieve ChEBI files (part of download)")
    def download_chebi(self):
        pbar = ProgressBar(maxval=4, widgets=["Downloading ChEBI files", Bar(), ETA()])
        pbar.start()
        retrieve_chebi_names()
        pbar.update(1)
        retrieve_chebi_relation()
        pbar.update(2)
        retrieve_chebi_vertice()
        pbar.update(3)
        retrieve_chebi_structures()
        pbar.update(4)
        pbar.finish()

    @expose(help="Retrieve DrugBank files (part of download)")
    def download_drug_bank(self):
        pbar = ProgressBar(maxval=2, widgets=["Downloading DrugBank files", Bar(), ETA()])
        pbar.start()
        retrieve_drugbank_open_structures(self.app.pargs.drugbank_version or "5.0.3")
        pbar.update(1)
        retrieve_drugbank_open_vocabulary(self.app.pargs.drugbank_version or "5.0.3")
        pbar.update(2)
        pbar.finish()

    @expose(help="Retrieve BIGG files (part of download)")
    def download_bigg(self):
        pbar = ProgressBar(maxval=2, widgets=["Downloading BIGG files", Bar(), ETA()])
        pbar.start()
        retrieve_bigg_reactions()
        pbar.update(1)
        retrieve_bigg_metabolites()
        pbar.update(2)
        pbar.finish()

    @expose(help="Retrieve PubChem files (part of download)")
    def download_pubchem(self):
        pubchem = parse_pubchem(os.path.join(internal_data_dir, "pubchem_compound_analogs_antimetabolites.txt"))
        pubchem_ids = pubchem.compound_id.unique()
        pbar = ProgressBar(maxval=len(pubchem_ids), widgets=["Downloading PubChem files",
                                                                              Bar(), ETA()])
        pbar.start()
        for i in retrieve_pubchem_mol_files(pubchem_ids, dest=data_dir):
            pbar.update(i)
        pbar.finish()

    @expose(help="Retrieve Zinc files (part of download)")
    def download_zinc(self):
        # retrieve_zinc_properties()
        retrieve_zinc_structures()

    @expose(help="Retrieve KEGG files (part of download)")
    def download_kegg(self):
        retrieve_kegg_brite()
        kegg = parse_kegg_brite(os.path.join(data_dir, "kegg_brite_08310.keg"))
        pbar = ProgressBar(maxval=len(kegg.kegg_drug_id.unique()), widgets=["Downloading KEGG files", Bar(), ETA()])
        pbar.start()
        for i in retrieve_kegg_mol_files(kegg, dest=data_dir):
            pbar.update(i)
        pbar.finish()

    @expose(help="Status of init")
    def status(self):
        necessary_files = ["chebi_names_3star.txt", "chebi_vertice_3star.tsv", "chebi_relation_3star.tsv",
                           "chebi_lite_3star.sdf", "kegg_brite_08310.keg", "drugbank_open_vocabulary.csv",
                           "drugbank_open_structures.sdf"]

        if self.app.pargs.with_zinc:
            necessary_files.append("zinc_16.sdf.gz",)

        missing = []

        for file_name in necessary_files:
            file_path = os.path.join(data_dir, file_name)

            if not os.path.isfile(file_path):
                missing.append(file_name)
                print(file_name.ljust(45) + "| FAIL: File does not exist")
            else:
                file_size = os.path.getsize(file_path)

                if file_size == 0:
                    missing.append(file_name)
                    print(file_name.ljust(45) + "| (%.1f MB) FAIL: File is too small" % (file_size / 1048576))
                else:
                    print(file_name.ljust(45) + "| (%.1f MB) OK" % (file_size / 1048576))

        return missing

    @expose(help="Build data (part of download)")
    def build_data(self):
        missing = self.status()
        if len(missing):
            print("Cannot continue without the missing files")
            exit(1)

        print("\nStart building data:")
        print("--------------------------------------------\n")
        print("Building ChEBI:")
        chebi_names_file = os.path.join(data_dir, "chebi_names_3star.txt")
        chebi_vertice_file = os.path.join(data_dir, "chebi_vertice_3star.tsv")
        chebi_relation_file = os.path.join(data_dir, "chebi_relation_3star.tsv")
        chebi_data = parse_chebi_data(chebi_names_file, chebi_vertice_file, chebi_relation_file)
        chebi_data.to_csv(os.path.join(data_dir, "chebi_analogues_filtered.csv"))
        print("Complete!")
        print("--------------------------------------------")
        print("Building PubChem:")
        pubchem = parse_pubchem(os.path.join(internal_data_dir, "pubchem_compound_analogs_antimetabolites.txt"))
        pubchem.to_csv(os.path.join(data_dir, "pubchem_data.csv"))
        print("Complete!")
        print("--------------------------------------------")
        print("Building KEGG:")
        kegg = parse_kegg_brite(os.path.join(data_dir, "kegg_brite_08310.keg"))
        kegg.to_csv(os.path.join(data_dir, "kegg_data.csv"))
        print("Complete!")

    @expose(help="Build database")
    def build_database(self):
        from marsi.io import data
        build_database(data, data_dir, self.app.pargs.with_zinc)

    @expose(help="Add known analogs")
    def add_known_analogs(self):
        chebi_client = ChEBI()
        print("Updating data from 'antimetabolites.xlsx'")

        anti_metabolites = read_excel(os.path.join(internal_data_dir, "antimetabolites.xlsx"), sheetname="Sheet1")
        anti_metabolites = anti_metabolites[anti_metabolites.Identifier != "?"]

        for _, row in anti_metabolites.iterrows():
            if row.Database == PUBCHEM_COMPOUND:
                temp_file = tempfile.mktemp(suffix="sdf", prefix=str(row.Identifier))
                pubchempy.download("SDF", temp_file, row.Identifier, overwrite=True)
                molecule = openbabel.sdf_to_molecule(temp_file)
                reference = Reference.add_reference("pubchem", str(row.Identifier))

            elif row.Database == CHEBI:
                entity = chebi_client.getCompleteEntity(row.Identifier)
                molecule = openbabel.mol_to_molecule(find_best_chebi_structure(entity), False)
                reference = Reference.add_reference("chebi", str(row.Identifier))
            else:
                print('{:16s}\t{:12s}\t{:25s}\t- Skip'.format(row.Database, str(row.Identifier), row.Target))
                continue

            synonym = Synonym.add_synonym(row.Name)
            try:
                Metabolite.get(inchi_key=openbabel.mol_to_inchi_key(molecule))
                print('{:16s}\t{:12s}\t{:25s}\t- OK'.format(row.Database, str(row.Identifier), row.Target))
            except KeyError:
                Metabolite.from_molecule(molecule, [reference], [synonym], analog=True, first_time=False)
                print('{:16s}\t{:12s}\t{:25s}\t- Added'.format(row.Database, str(row.Identifier), row.Target))
