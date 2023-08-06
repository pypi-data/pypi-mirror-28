""" Class for downloading and loading required external resources.

`lineage` uses tables and data from UCSC's Genome Browser:

* http://genome.ucsc.edu/
* http://genome.ucsc.edu/cgi-bin/hgTables

References
----------
..[1] Karolchik D, Hinrichs AS, Furey TS, Roskin KM, Sugnet CW, Haussler D, Kent WJ.
  The UCSC Table Browser data retrieval tool. Nucleic Acids Res. 2004 Jan
  1;32(Database issue):D493-6. PubMed PMID: 14681465; PubMed Central PMCID:
  PMC308837. https://www.ncbi.nlm.nih.gov/pubmed/14681465
..[2] Tyner C, Barber GP, Casper J, Clawson H, Diekhans M, Eisenhart C, Fischer CM,
  Gibson D, Gonzalez JN, Guruvadoo L, Haeussler M, Heitner S, Hinrichs AS,
  Karolchik D, Lee BT, Lee CM, Nejad P, Raney BJ, Rosenbloom KR, Speir ML,
  Villarreal C, Vivian J, Zweig AS, Haussler D, Kuhn RM, Kent WJ. The UCSC Genome
  Browser database: 2017 update. Nucleic Acids Res. 2017 Jan 4;45(D1):D626-D634.
  doi: 10.1093/nar/gkw1134. Epub 2016 Nov 29. PubMed PMID: 27899642; PubMed Central
  PMCID: PMC5210591. https://www.ncbi.nlm.nih.gov/pubmed/27899642
..[3] International Human Genome Sequencing Consortium. Initial sequencing and
  analysis of the human genome. Nature. 2001 Feb 15;409(6822):860-921.
  http://dx.doi.org/10.1038/35057062
..[4] hg19 (GRCh37): Hiram Clawson, Brooke Rhead, Pauline Fujita, Ann Zweig, Katrina
  Learned, Donna Karolchik and Robert Kuhn, https://genome.ucsc.edu/cgi-bin/hgGateway?db=hg19

"""

"""
Copyright (C) 2017 Andrew Riha

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import gzip
import os
import tarfile
import urllib.request
import zlib

import pandas as pd

import lineage


class Resources(object):
    """ Object used to manage resources required by `lineage`. """

    def __init__(self, resources_dir):
        """ Initialize a ``Resources`` object.

        Parameters
        ----------
        resources_dir : str
            name / path of resources directory

        """
        self._resources_dir = os.path.abspath(resources_dir)
        self._hapmap_h37 = None
        self._cytoband_h37 = None
        self._knownGene_h37 = None
        self._kgXref_h37 = None

    def get_hapmap_h37(self):
        """ Get International HapMap Consortium HapMap for Build 37.

        Returns
        -------
        dict
            dict of pandas.DataFrame HapMap tables if loading was successful, else None

        """
        if self._hapmap_h37 is None:
            self._hapmap_h37 = self._load_hapmap(self._get_path_hapmap_h37())

        return self._hapmap_h37

    def get_cytoband_h37(self):
        """ Get UCSC cytoBand table for Build 37.

        Returns
        -------
        pandas.DataFrame
            cytoBand table if loading was successful, else None

        """
        if self._cytoband_h37 is None:
            self._cytoband_h37 = self._load_cytoband(self._get_path_cytoband_h37())

        return self._cytoband_h37

    def get_knownGene_h37(self):
        """ Get UCSC knownGene table for Build 37.

        Returns
        -------
        pandas.DataFrame
            knownGene table if loading was successful, else None

        """
        if self._knownGene_h37 is None:
            self._knownGene_h37 = self._load_knownGene(self._get_path_knownGene_h37())

        return self._knownGene_h37

    def get_kgXref_h37(self):
        """ Get UCSC kgXref table for Build 37.

        Returns
        -------
        pandas.DataFrame
            kgXref table if loading was successful, else None

        """
        if self._kgXref_h37 is None:
            self._kgXref_h37 = self._load_kgXref(self._get_path_kgXref_h37())

        return self._kgXref_h37

    def download_example_datasets(self):
        """ Download example datasets from `openSNP <https://opensnp.org>`_.

        Per openSNP, "the data is donated into the public domain using `CC0 1.0
        <http://creativecommons.org/publicdomain/zero/1.0/>`_."

        References
        ----------
        ..[1] Greshake B, Bayer PE, Rausch H, Reda J (2014), "openSNP–A Crowdsourced Web Resource
          for Personal Genomics," PLOS ONE, 9(3): e89204,
          https://doi.org/10.1371/journal.pone.0089204

        """
        self._download_file(self._get_url_dataset_user662_304(),
                            '662.23andme.304.csv.gz', compress=True)
        self._download_file(self._get_url_dataset_user662_340(),
                            '662.23andme.340.csv.gz', compress=True)
        self._download_file(self._get_url_dataset_user662_341(),
                            '662.ftdna-illumina.341.csv.gz', compress=True)
        self._download_file(self._get_url_dataset_user663_305(),
                            '663.23andme.305.csv.gz', compress=True)

        # these two files consist of concatenated gzip files and therefore need special handling
        gzip_paths = []
        gzip_paths.append(self._download_file(self._get_url_dataset_user4583_3482(),
                                              '4583.ftdna-illumina.3482.csv.gz'))
        gzip_paths.append(self._download_file(self._get_url_dataset_user4584_3483(),
                                              '4584.ftdna-illumina.3483.csv.gz'))

        try:
            for gzip_path in gzip_paths:
                # https://stackoverflow.com/q/4928560
                # https://stackoverflow.com/a/37042747
                with open(gzip_path, 'rb') as f:
                    decompressor = zlib.decompressobj(31)

                    # decompress data from first concatenated gzip file
                    data = decompressor.decompress(f.read())

                    if len(decompressor.unused_data) > 0:
                        # decompress data from second concatenated gzip file, if any
                        additional_data = zlib.decompress(decompressor.unused_data, 31)
                        data += additional_data[33:]  # skip over second header

                # recompress data
                with gzip.open(gzip_path, 'wb') as f:
                    f.write(data)
        except Exception as err:
            print(err)

    @staticmethod
    def _get_url_dataset_user662_304():
        return 'https://opensnp.org/data/662.23andme.304'

    @staticmethod
    def _get_url_dataset_user662_340():
        return 'https://opensnp.org/data/662.23andme.340'

    @staticmethod
    def _get_url_dataset_user662_341():
        return 'https://opensnp.org/data/662.ftdna-illumina.341'

    @staticmethod
    def _get_url_dataset_user663_305():
        return 'https://opensnp.org/data/663.23andme.305'

    @staticmethod
    def _get_url_dataset_user4583_3482():
        return 'https://opensnp.org/data/4583.ftdna-illumina.3482'

    @staticmethod
    def _get_url_dataset_user4584_3483():
        return 'https://opensnp.org/data/4584.ftdna-illumina.3483'

    @staticmethod
    def _load_hapmap(filename):
        """ Load HapMap.

        Parameters
        ----------
        filename : str
            path to compressed archive with HapMap data

        Returns
        -------
        hapmap : dict
            dict of pandas.DataFrame HapMap tables if loading was successful, else None

        """
        if filename is None:
            return None

        try:
            hapmap = {}

            if '37' in filename:
                with tarfile.open(filename, 'r') as tar:
                    # http://stackoverflow.com/a/2018576
                    for member in tar.getmembers():
                        if 'genetic_map' in member.name:
                            df = pd.read_csv(tar.extractfile(member), sep='\t')
                            df = df.rename(columns={'Position(bp)': 'pos',
                                                    'Rate(cM/Mb)': 'rate',
                                                    'Map(cM)': 'map'})
                            del df['Chromosome']
                            start_pos = member.name.index('chr') + 3
                            end_pos = member.name.index('.')
                            hapmap[member.name[start_pos:end_pos]] = df
            else:
                hapmap = None
        except Exception as err:
            print(err)
            hapmap = None

        return hapmap

    @staticmethod
    def _load_cytoband(filename):
        """ Load UCSC cytoBand table.

        Parameters
        ----------
        filename : str
            path to cytoBand file

        Returns
        -------
        df : pandas.DataFrame
            cytoBand table if loading was successful, else None

        References
        ----------
        ..[1] Ryan Dale, GitHub Gist,
          https://gist.github.com/daler/c98fc410282d7570efc3#file-ideograms-py

        """
        if filename is None:
            return None

        try:
            # adapted from chromosome plotting code (see [1]_)
            df = pd.read_table(filename, names=['chrom', 'start', 'end', 'name', 'gie_stain'])
            df['chrom'] = df['chrom'].str[3:]
            return df
        except Exception as err:
            print(err)
            return None

    @staticmethod
    def _load_knownGene(filename):
        """ Load UCSC knownGene table.

        Parameters
        ----------
        filename : str
            path to knownGene file

        Returns
        -------
        df : pandas.DataFrame
            knownGene table if loading was successful, else None
        """
        if filename is None:
            return None

        try:
            df = pd.read_table(filename, names=['name', 'chrom', 'strand', 'txStart', 'txEnd',
                                                'cdsStart', 'cdsEnd', 'exonCount', 'exonStarts',
                                                'exonEnds', 'proteinID', 'alignID'], index_col=0)
            df['chrom'] = df['chrom'].str[3:]
            return df
        except Exception as err:
            print(err)
            return None

    @staticmethod
    def _load_kgXref(filename):
        """ Load UCSC kgXref table.

        Parameters
        ----------
        filename : str
            path to kgXref file

        Returns
        -------
        df : pandas.DataFrame
            kgXref table if loading was successful, else None
        """
        if filename is None:
            return None

        try:
            df = pd.read_table(filename, names=['kgID', 'mRNA', 'spID', 'spDisplayID',
                                                'geneSymbol', 'refseq', 'protAcc',
                                                'description', 'rfamAcc', 'tRnaName'], index_col=0,
                               dtype=object)
            return df
        except Exception as err:
            print(err)
            return None

    def _get_path_cytoband_h37(self):
        """ Get local path to cytoBand file for hg19 / GRCh37 from UCSC, downloading if necessary.

        Returns
        -------
        str
            path to cytoband_h37.txt.gz

        """

        return self._download_file(self._get_url_cytoband_h37(), 'cytoband_h37.txt.gz')

    @staticmethod
    def _get_url_cytoband_h37():
        return 'ftp://hgdownload.cse.ucsc.edu/goldenPath/hg19/database/cytoBand.txt.gz'

    def _get_path_hapmap_h37(self):
        """ Get local path to HapMap for hg19 / GRCh37, downloading if necessary.

        Returns
        -------
        str
            path to hapmap_h37.tar.gz

        References
        ----------
        ..[1] "The International HapMap Consortium (2007).  A second generation human haplotype
          map of over 3.1 million SNPs.  Nature 449: 851-861."
        ..[2] "The map was generated by lifting the HapMap Phase II genetic map from build 35 to
          GRCh37. The original map was generated using LDhat as described in the 2007 HapMap
          paper (Nature, 18th Sept 2007). The conversion from b35 to GRCh37 was achieved using
          the UCSC liftOver tool. Adam Auton, 08/12/2010"

        """

        return self._download_file(self._get_url_hapmap_h37(), 'hapmap_h37.tar.gz')

    @staticmethod
    def _get_url_hapmap_h37():
        return 'ftp://ftp.ncbi.nlm.nih.gov/hapmap/recombination/2011-01_phaseII_B37/' \
               'genetic_map_HapMapII_GRCh37.tar.gz'

    def _get_path_knownGene_h37(self):
        """ Get local path to knownGene file for hg19 / GRCh37 from UCSC, downloading if necessary.

        Returns
        -------
        str
            path to knownGene_h37.txt.gz

        """

        return self._download_file(self._get_url_knownGene_h37(), 'knownGene_h37.txt.gz')

    @staticmethod
    def _get_url_knownGene_h37():
        return 'ftp://hgdownload.cse.ucsc.edu/goldenPath/hg19/database/knownGene.txt.gz'


    def _get_path_kgXref_h37(self):
        """ Get local path to kgXref file for hg19 / GRCh37 from UCSC, downloading if necessary.

        Returns
        -------
        str
            path to kgXref_h37.txt.gz

        """

        return self._download_file(self._get_url_kgXref_h37(), 'kgXref_h37.txt.gz')

    @staticmethod
    def _get_url_kgXref_h37():
        return 'ftp://hgdownload.cse.ucsc.edu/goldenPath/hg19/database/kgXref.txt.gz'

    def _download_file(self, url, filename, compress=False):
        """ Download a file to the resources folder.

        Download data from `url`, save as `filename`, and optionally compress with gzip.

        Parameters
        ----------
        url : str
            URL to download data from
        filename : str
            name of file to save; if compress, ensure '.gz' is appended
        compress : bool
            compress with gzip

        Returns
        -------
        str
            path to downloaded file, None if error

        """
        if not lineage.create_dir(self._resources_dir):
            return None

        if compress and filename[-3:] != '.gz':
            filename += '.gz'

        destination = os.path.join(self._resources_dir, filename)

        if not os.path.exists(destination):
            try:
                self._print_download_msg(destination)

                if compress:
                    open_func = gzip.open
                else:
                    open_func = open

                # get file if it hasn't already been downloaded
                # http://stackoverflow.com/a/7244263
                with urllib.request.urlopen(url) as response, open_func(destination, 'wb') as f:
                    data = response.read()  # a `bytes` object
                    f.write(data)
            except Exception as err:
                print(err)
                return None

        return destination

    @staticmethod
    def _print_download_msg(path):
        """ Print download message.

        Parameters
        ----------
        path : str
            path to file being downloaded
        """
        print('Downloading ' + os.path.relpath(path))
