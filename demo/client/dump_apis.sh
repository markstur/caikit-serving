#!/usr/bin/env bash

# Make a directory with interfaces
generated_interfaces="$(pwd)/generated_interfaces"
echo "Creating output dir:  ${generated_interfaces}"
mkdir -p $generated_interfaces

# Dump the gRPC interfaces (using caikit as configured)
cd ../..
echo "Using caikit.runtime.dump_services to get interfaces"
RUNTIME_LIBRARY=caikit_embeddings python -m caikit.runtime.dump_services $generated_interfaces
