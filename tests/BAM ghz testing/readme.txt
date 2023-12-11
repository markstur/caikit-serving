The BAM ghz testing tooling is designed to be run in the BAM cluster.
There are hardcoded values, endpoints, certs being used, etc...

To run tests, do the following:
1. Clone the repo locally
2. Log into the BAM cluster locally
3. Determine the pod you want to act as the ghz-client-pod (it should NOT be a model serving pod being tested!)
4. oc rsync .../perf-ghz ghz-client-pod:/tmp
5. Within the ghz-client-pod, go into its terminal, cd /tmp/perf-ghz directory
6. To execute the tests run: nohup ./embeddings-perf-test-suite.sh &
7. Capture test results within the nohup.out file