#!/usr/bin/env bash

set -eux
pwd

# activate virtualenv
source azEnv/bin/activate

# remove extension
echo "Remove existing aks-preview extension (if any)"
if az extension remove --name aks-preview || azdev extension remove aks-preview; then
    deactivate
    source azEnv/bin/activate
fi

# test cli
if [[ $TEST_MODE == "record" || $TEST_MODE == "all" ]]; then
    echo "Test in record mode!"
    azdev test acs --no-exitfirst --xml-path cli_result.xml --discover -a "-n $PARALLELISM --json-report --json-report-file=cli_report.json --reruns 3 --capture=sys"
    cp *cli_report.json *cli_result.xml reports/
fi

if [[ $TEST_MODE == "live" || $TEST_MODE == "all" ]]; then
    echo "Test in live mode!"
    az login --service-principal -u $AZCLI_ALT_CLIENT_ID -p $AZCLI_ALT_CLIENT_SECRET -t $TENANT_ID
    az account set -s $AZCLI_ALT_SUBSCRIPTION_ID
    az account show
    azdev test acs --live --no-exitfirst --xml-path cli_live_result.xml --discover -a "-n $PARALLELISM --json-report --json-report-file=cli_live_report.json --reruns 3 --capture=sys"
    cp *cli_live_report.json *cli_live_result.xml reports/
fi
