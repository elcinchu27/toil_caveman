"""toil_caveman commands."""

from glob import glob
from os.path import join
import os
import subprocess

from toil.common import Toil
from toil_container import ContainerArgumentParser
from toil_container import ContainerJob

from toil_caveman import __version__

ARGUMENTS = [
    'annot-bed-files',
    'species-assembly',
    'flag-bed-files',
    'flagConfig',
    'flagToVcfConfig',
    'germline-indel',
    'ignore-file',
    'norm-cn-default',
    'normal-bam',
    'normal-cn',
    'normal-contamination',
    'normal-protocol',
    'outdir',
    'reference',
    'seqType',
    'species',
    'tum-cn-default',
    'tumour-bam',
    'tumour-cn',
    'tumour-protocol',
    'unmatched-vcf']


class StepRunner(ContainerJob):

    def __init__(self, process, options, index=1, **kwargs):
        """
        Add the caveman process and index as attributes.

        Arguments:
            kwargs (dict): extra ContainerJob key word arguments.
            process (str): see caveman.pl --help.
            index (int): caveman process index.
            options (object): caveman process index.
        """
        self.process = process
        self.index = index
        super(StepRunner, self).__init__(
            unitName='Caveman%s %s' % (process.capitalize(), index),
            displayName='Caveman%s' % process.capitalize(),
            memory=options.max_memory_usage or kwargs.pop('memory', '10G'),
            options=options,
            cores=kwargs.pop('cores', 1),
            **kwargs)

    def run(self, fileStore):
        cmd = [
            'caveman.pl',
            '-process', self.process,
            '-index', self.index,
            '-threads', self.cores,
            '-logs', join(self.options.outdir, "clogs")]

        for i in ARGUMENTS:
            value = getattr(self.options, i.replace('-', '_'), None)

            if value:
                cmd += ['-' + i, value]

        # run the command and allow file system to register output files
        cmd = list(map(str, cmd))
        self.call(cmd, cwd=self.options.outdir)
        fileStore.logToMaster("\n\nRan: " + " ".join(cmd))


class Split(ContainerJob):

    def run(self, fileStore):
        with open(self.options.reference) as f:
            for ix, i in enumerate(f):
                if i.strip():
                    self.addChild(StepRunner(
                        process='split',
                        index=ix + 1,
                        options=self.options))


class RemoveContigs(ContainerJob):

    def run(self, fileStore):
        tmpdir = join(self.options.outdir, 'tmpCaveman')
        delete = list(glob(join(tmpdir, 'splitList.GL*')))
        delete.extend(glob(join(tmpdir, 'splitList.hs*')))
        delete.extend(glob(join(tmpdir, 'splitList.MT')))
        delete.extend(glob(join(tmpdir, 'splitList.NC*')))

        for i in delete:
            try:
                os.remove(i)
            except:  # pylint: disable=W0702
                pass


class SplitRunner(ContainerJob):

    def __init__(self, process, **kwargs):
        self.process = process
        super(SplitRunner, self).__init__(**kwargs)

    def split_list_range(self):
        with open(join(self.options.outdir, 'tmpCaveman', 'splitList')) as f:
            count = 0
            for i in f:
                if i.strip():
                    count += 1
                    yield count

    def run(self, fileStore):
        for i in self.split_list_range():
            self.addChild(StepRunner(
                process=self.process,
                runtime=59,
                index=i,
                options=self.options))


def run_toil(options):
    """Toil implementation for cgpCaveman."""
    defaults = dict(runtime=59, options=options)
    setup = StepRunner(process='setup', **defaults)
    split = Split(**defaults)
    remove = RemoveContigs(**defaults)
    concat = StepRunner(process='split_concat', **defaults)
    mstep = SplitRunner(process='mstep', **defaults)
    merge = StepRunner(process='merge', **defaults)
    estep = SplitRunner(process='estep', **defaults)
    results = StepRunner(process='merge_results', **defaults)
    add_ids = StepRunner(process='add_ids', **defaults)
    flag = StepRunner(process='flag', options=options)

    # build dag
    setup.addFollowOn(split)
    split.addFollowOn(remove)
    remove.addFollowOn(concat)
    concat.addFollowOn(mstep)
    mstep.addFollowOn(merge)
    merge.addFollowOn(estep)
    estep.addFollowOn(results)
    results.addFollowOn(add_ids)
    add_ids.addFollowOn(flag)

    with Toil(options) as pipe:
        if not pipe.options.restart:
            pipe.start(setup)
        else:
            pipe.restart()


def get_parser():
    """Get pipeline configuration using toil's argparse."""
    parser = ContainerArgumentParser(version=__version__)
    parser.description = 'Run toil_pindel pipeline.'
    settings = parser.add_argument_group('See caveman.pl --help.')

    for i in ARGUMENTS:
        settings.add_argument('--' + i, required=False, default=None)

    settings.add_argument(
        '--max_memory_usage',
        help='max ram usage e.g. 1G, 1000M',
        default=None)

    return parser


def process_parsed_options(options):
    """Process parsed options."""
    validate_bam(options.tumour_bam)
    validate_bam(options.normal_bam)
    validate_reference(options.reference)

    if options.writeLogs is not None:
        subprocess.check_call(['mkdir', '-p', options.writeLogs])

    return options


def main():
    """Parse options and run toil."""
    options = get_parser().parse_args()
    options = process_parsed_options(options=options)
    run_toil(options)


def validate_reference(value):
    """Make sure the passed reference has an index file."""
    value = os.path.abspath(value)

    if not value.endswith('.fai'):
        raise Exception(value + ' must end in .fai.')

    return value

def validate_bam(value):
    """Make sure the passed bam has an index file."""
    value = os.path.abspath(value)
    index = str(value) + '.bai'

    if not os.path.isfile(index):
        raise Exception(index + ' should be an existing file.')

    return value
