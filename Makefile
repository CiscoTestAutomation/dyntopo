################################################################################
#                        Dyntopo Makefile
#
# Author:
#   pyats-support-ext@cisco.com
#
# Support:
#   pyats-support-ext@cisco.com
#
# Version:
#   v1.0
#
# Date:
#   December 2020
#
# About This File:
#   This script will build the documentation of the Dyntopo package which could
#   be served locally via make serve
#
# Requirements:
#	1. Please install dependencies via the make install_build_deps command first
################################################################################

# Variables
PKG_NAME      = dyntopo
BUILDDIR      = $(shell pwd)/__build__/documentation
HOSTNAME	  = localhost

DEPENDENCIES = robotframework Sphinx sphinxcontrib-napoleon \
			   sphinxcontrib-mockautodoc sphinx-rtd-theme

.PHONY: help install_build_deps docs serve clean

help:
	@echo "Please use 'make <target>' where <target> is one of"
	@echo ""
	@echo "docs:            	Build Sphinx documentation for this package"
	@echo "clean: 			Remove generated documentation"
	@echo "install_build_deps: 	Install build dependencies for docs"
	@echo ""
	@echo "     --- default Sphinx targets ---"
	@echo ""
	@echo "serve:      		to start a web server to serve generated html files"

install_build_deps:
	@echo "Installing build dependecies into your environment"
	@pip install $(DEPENDENCIES)
	@echo ""
	@echo "Successfully installed build dependencies"

clean:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Removing build artifacts ..."
	@./setup.py clean
	@echo ""
	@echo "Done."
	@echo ""

docs:
	@echo ""
	@echo "--------------------------------------------------------------------"
	@echo "Building $(PKG_NAME) documentation for preview: $@"
	@echo ""

	@./setup.py docs

	@echo "Completed building docs for preview."
	@echo ""

serve:
	@echo "point your browser to http://$(HOSTNAME):8000"
	@cd $(BUILDDIR)/html && python -m http.server || echo Error: run \'make \
	docs\' before using \'make serve\'
