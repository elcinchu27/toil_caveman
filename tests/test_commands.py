"""Tests for toil_caveman."""

from os.path import abspath
from os.path import dirname
from os.path import join
from os.path import isfile

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
        '--germline-indel', join(DATA, 'caveman', 'germline_indel.bed.gz'),
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


def test_version():
    """Sample test for the __version__ variable."""
    assert __version__
