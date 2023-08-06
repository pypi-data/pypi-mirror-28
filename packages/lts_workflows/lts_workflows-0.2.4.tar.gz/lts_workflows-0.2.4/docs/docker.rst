.. _docker:

Docker images
==============

:mod:`lts-workflows` includes a docker image `percyfal/lts-workflows`
that serves as a base image for workflows in the :mod:`lts-workflows`
package. It is configured to be fairly lean, containing packages for
reproducible research and literate programming using R and Rmarkdown.
Workflows that provide docker images should use
`percyfal/lts-workflows` as the starting image.
