#SHELL := bash
#.ONESHELL:
#.SHELLFLAGS := -eu -o pipefail

ICENET_ENV?=dev
ICENET_AZ_APPLICATION?=web-icenet$(ICENET_ENV)-application
ICENET_GH_APPLICATION?=https://github.com/icenet-ai/icenet-application
ICENET_RG?=rg-icenet$(ICENET_ENV)-webapps

.PHONY: clean deploy-azure run

clean:

deploy-azure:
	az webapp deployment source config --branch main --manual-integration --name $(ICENET_AZ_APPLICATION) --repo-url $(ICENET_GH_APPLICATION) --resource-group $(ICENET_RG)

sync-deployment:
	az webapp deployment source sync --name $(ICENET_AZ_APPLICATION) --resource-group $(ICENET_RG)

run:
	gunicorn icenet_app.app:app
