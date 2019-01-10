# toil_caveman

[![pypi badge][pypi_badge]][pypi_base]
[![travis badge][travis_badge]][travis_base]
[![codecov badge][codecov_badge]][codecov_base]
[![docker badge][docker_badge]][docker_base]
[![docker badge][automated_badge]][docker_base]
[![code formatting][black_badge]][black_base]

A toil wrapper for cgpCaveman.

## Usage

This package uses docker to manage its dependencies, there are 2 ways of using it:

1. Running the [container][docker_base] in single machine mode without [`--batchSystem`] support:

        # using docker
        docker run -it papaemmelab/toil_caveman --help

        # using singularity
        singularity run docker://papaemmelab/toil_caveman --help

1. Installing the python package from [pypi][pypi_base] and passing the container as a flag:

        # install package
        pip install toil_caveman

        # run with docker
        toil_caveman [TOIL-OPTIONS] [PIPELINE-OPTIONS]
            --docker papaemmelab/toil_caveman
            --volumes <local path> <container path>
            --batchSystem LSF

        # run with singularity
        toil_caveman [TOIL-OPTIONS] [PIPELINE-OPTIONS]
            --singularity docker://papaemmelab/toil_caveman
            --volumes <local path> <container path>
            --batchSystem LSF

See [docker2singularity] if you want to use a [singularity] image instead of using the `docker://` prefix.

## Contributing

Contributions are welcome, and they are greatly appreciated, check our [contributing guidelines](.github/CONTRIBUTING.md)!

## Credits

This package was created using [Cookiecutter] and the
[papaemmelab/cookiecutter-toil] project template.

[singularity]: http://singularity.lbl.gov/
[docker2singularity]: https://github.com/singularityware/docker2singularity
[cookiecutter]: https://github.com/audreyr/cookiecutter
[papaemmelab/cookiecutter-toil]: https://github.com/papaemmelab/cookiecutter-toil
[`--batchSystem`]: http://toil.readthedocs.io/en/latest/developingWorkflows/batchSystem.html?highlight=BatchSystem
[docker_base]: https://hub.docker.com/r/papaemmelab/toil_caveman
[docker_badge]: https://img.shields.io/docker/build/papaemmelab/toil_caveman.svg
[automated_badge]: https://img.shields.io/docker/automated/papaemmelab/toil_caveman.svg
[codecov_badge]: https://codecov.io/gh/papaemmelab/toil_caveman/branch/master/graph/badge.svg
[codecov_base]: https://codecov.io/gh/papaemmelab/toil_caveman
[pypi_badge]: https://img.shields.io/pypi/v/toil_caveman.svg
[pypi_base]: https://pypi.python.org/pypi/toil_caveman
[travis_badge]: https://img.shields.io/travis/papaemmelab/toil_caveman.svg
[travis_base]: https://travis-ci.org/papaemmelab/toil_caveman
[black_badge]: https://img.shields.io/badge/code%20style-black-000000.svg
[black_base]: https://github.com/ambv/black
