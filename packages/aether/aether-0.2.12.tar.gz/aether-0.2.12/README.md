# Welcome to Aether

The Aether platform is a system of applications and utilities for developers to rapidly and easily build algorithms
that use satellite and geospatial data. The Aether platform is accessible by REST API and python, but operates
entirely in the cloud using deferred graphs. This allows developers to build and execute applications with processing
abstracted away and minimal data transfer. An important consequence of this design choice is that the same algorithm
code developers use during exploration can be repackaged and deployed as mobile or web applications. These
applications are entirely portable, and can be published to users or other developers through a simple URL key.
In that regard, the Aether platform is an SDK for satellite analytics and framework for mobile end user applications.

The platform currently supports search of three publicly available Resources: The LandSat Archive (LandSat 4
through 8), Sentinel-2, and the USDA Cropland Data Layer, a 30m map of the US categorizing the agricultural land use
annually.

The platform is designed to rapidly add new data layers, making them available through the same interface. Resources
can be hosted by Aether, or made accessible via owner API, and restricted to a subset of users. The usage of each
Resource and its geographic usage is tracked as well.

The Aether platform is designed to allow user-developers to compile and publish their applications as easily as they
prototype, often with the same code. This tutorial demonstrates a developer creating an application that generates
an NDVI map from LandSat imagery for an arbitrary polygon, which does not need to be specified until runtime by
the end user (or mobile device).
