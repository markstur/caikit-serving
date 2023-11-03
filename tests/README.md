# Running performance tests for caikit-embeddings


## Test Setup

Copy and fill the env-example file, then export variables.
```sh
export $(cat .env | xargs)
```

## Running the Tests

Run tests for latency.
```sh
python simple-throughput-test.py
```

Run tests for throughput.

```sh
python simple-latency-test.py
```

## Test Results

The results will be printed at the terminal by the end of execution.
```sh
**** LATENCY TEST REPORT ****
Iterations:  100
Min Latency: 5.78  Sec
Max Latency: 11.57  Sec
25 Percentile: 7.2  Sec
50 Percentile: 7.66  Sec
75 Percentile: 8.45  Sec
90 Percentile: 9.19  Sec
99 Percentile: 10.16  Sec
Average Latency: 7.83  Sec

**** THROUGHPUT TEST REPORT ****
Total Requests:  100
Requests per Sec:  2
Requests Served:  100
Min Latency: 9.39  Sec
Max Latency: 525.93  Sec
25 Percentile: 130.84  Sec
50 Percentile: 275.2  Sec
75 Percentile: 418.41  Sec
90 Percentile: 483.86  Sec
99 Percentile: 519.98  Sec
Average Latency: 275.35  Sec
Throughput:  0.17 Requests/Sec
```