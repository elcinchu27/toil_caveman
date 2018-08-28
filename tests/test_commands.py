"""Tests for toil_caveman."""

from os.path import abspath
from os.path import dirname
from os.path import join
from os.path import isfile
from glob import glob

import pytest

from toil_caveman import commands
from toil_caveman import __version__

DATA = join(abspath(dirname(__file__)), "data")


def test_caveman(tmpdir):
    """
    Sample test for the main command.

    Test bams include a short region in chr 21 (takes ~5mins to run pipeline).
    Environment variables are set in pytest.ini. pytest-env must be installed.
    """
    args = [
        join(str(tmpdir), 'jobstore'),
        '--max_memory_usage', '1',
        '--outdir', tmpdir.strpath,
        '--reference', join(DATA, 'reference', 'reference.fasta.fai'),
        '--tumour-bam', join(DATA, 'tumor', 'tumor.bam'),
        '--normal-bam', join(DATA, 'normal', 'normal.bam'),
        '--species', 'Human',
        '--species-assembly', 'GRCh37d5',
        '--germline-indel', join(DATA, 'caveman', 'germline_indel.bed'),
        '--unmatched-vcf', join(DATA, 'caveman'),
        '--normal-cn', join(DATA, 'caveman', 'caveman_cn.txt'),
        '--tumour-cn', join(DATA, 'caveman', 'caveman_cn.txt'),
        '--norm-cn-default', '2',
        '--tum-cn-default', '2',
        '--ignore-file', join(DATA, 'caveman', 'ignore.txt'),
        '--seqType', 'genome',
        '--flag-bed-files', join(DATA, 'flagging')]

    parser = commands.get_parser()
    options = parser.parse_args(args)
    options = commands.process_parsed_options(options)
    commands.run_toil(options)
    expected = join(tmpdir.strpath, 'tumor_vs_normal.flagged.muts.vcf.gz')
    assert isfile(expected), 'Missing expected output: ' + expected


@pytest.mark.skipif(True,reason="Un comment this skip.")
def test_caveman_at_juno(tmpdir):
    """
    Sample test for the main command.

    Test bams include a short region in chr 21 (takes ~5mins to run pipeline).
    Environment variables are set in pytest.ini. pytest-env must be installed.
    """
    args = [
        '/work/leukgen/home/leukbot/tests/toil_caveman/outdir/jobstore', '--stats', '--disableChaining', '--restart',
        '--maxLocalJobs', '2000',
        '--statePollingWait', '300',
        '--batchSystem', 'CustomLSF',
        '--singularity', '/work/leukgen/home/leukbot/leukgen_docker-cgp-2018-08-28-dc4658bd6f58.img',
        '--volumes', '/juno', '/juno',
        '--volumes', '/ifs', '/ifs',
        '--volumes', '/work', '/work',
        '--outdir', '/work/leukgen/home/leukbot/tests/toil_caveman/outdir',
        '--reference', '/ifs/work/leukgen/ref/homo_sapiens/GRCh37d5/genome/gr37.fasta.fai',
        '--tumour-bam', '/ifs/res/leukgen/local/opt/leukdc/data/workflows/03/85/40385/data/bam/I-H-134255-T5-1-D1-1.bam',
        '--normal-bam', '/ifs/res/leukgen/local/opt/leukdc/data/workflows/03/93/40393/data/bam/I-H-134255-N1-1-D1-1.bam',
        '--species', 'Human',
        '--species-assembly', 'GRCh37d5',
        '--germline-indel', '/ifs/res/leukgen/local/opt/leukdc/data/analyses/21/09/112109/output/I-H-134255-T5-1-D1-1_vs_I-H-134255-N1-1-D1-1.germline.bed',
        '--unmatched-vcf', '/ifs/work/leukgen/ref/homo_sapiens/GRCh37d5/caveman/unmatched_normal_panel_bwamem_mapped_with_xten',
        '--normal-cn', '/ifs/res/leukgen/local/opt/leukdc/data/analyses/22/52/112252/output/I-H-134255-T5-1-D1-1_caveman_normal_cn_input.txt',
        '--tumour-cn', '/ifs/res/leukgen/local/opt/leukdc/data/analyses/22/52/112252/output/I-H-134255-T5-1-D1-1_caveman_tumour_cn_input.txt',
        '--norm-cn-default', '2',
        '--tum-cn-default', '5',
        '--ignore-file', '/ifs/work/leukgen/ref/homo_sapiens/GRCh37d5/caveman/genome.gap.tab',
        '--seqType', 'genomic',
        '--flag-bed-files', '/ifs/work/leukgen/ref/homo_sapiens/GRCh37d5/caveman/flagging',
        '--flagToVcfConfig', '/ifs/work/leukgen/ref/homo_sapiens/GRCh37d5/caveman/flagging/flag.to.vcf.convert.ini',
        '--flagConfig', '/ifs/work/leukgen/ref/homo_sapiens/GRCh37d5/caveman/flagging/flag.vcf.config.ini',
        '--normal-contamination', '0.15094',
        ]

    parser = commands.get_parser()
    options = parser.parse_args(args)
    options = commands.process_parsed_options(options)
    commands.run_toil(options)
    assert glob('/work/leukgen/home/leukbot/tests/toil_caveman/outdir/*.flagged.muts.vcf.gz')


def test_version():
    """Sample test for the __version__ variable."""
    assert __version__
