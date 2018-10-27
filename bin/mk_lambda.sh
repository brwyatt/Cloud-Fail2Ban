#!/bin/bash

dir="$(dirname "$(dirname "$(readlink -f $0)")")"
build_dir="${dir}/build"
lambda_zip="${build_dir}/lambda.zip"
lambda_dir="${dir}/lambda"
modules_dir="${dir}/src"
# dependencies_dir="${dir}/deps"

mkdir -p "${build_dir}"
rm -f "${lambda_zip}"

cd "${lambda_dir}"
zip -r "${lambda_zip}" * -i "*.py"

cd "${modules_dir}"
zip -r "${lambda_zip}" * -i "*.py"
