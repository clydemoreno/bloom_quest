import http from 'k6/http';
import { sleep, check } from 'k6';
import { Trend, Rate } from 'k6/metrics';

// Define custom metrics for usebloom=1
const responseTimesWithBloom = new Trend('response_times_with_bloom');
const errorRateWithBloom = new Rate('error_rate_with_bloom');

// Define the maximum acceptable response time threshold (in milliseconds)
const maxResponseTimeThreshold = 10000; // 10,000 milliseconds (10 seconds)

export const options = {
  thresholds: {
    // Define a threshold for the maximum response time not to exceed maxResponseTimeThreshold
    'http_req_duration{max}': [`<=${maxResponseTimeThreshold}`],
  },
};

export default function () {
  let randomOrderId;
  const randomValue = Math.random();

  if (randomValue <= 0.05) {
    randomOrderId = Math.floor(Math.random() * 201) + 1;
  } else {
    randomOrderId = Math.floor(Math.random() * 9800) + 201;
  }

  // Test with usebloom=1
  const urlWithBloom = `http://127.0.0.1:5000/orders/${randomOrderId}?usebloom=1`;
  const responseWithBloom = http.get(urlWithBloom);
  check(responseWithBloom, {
    'is status 200': (r) => r.status === 200,
    'is status 404': (r) => r.status === 404,
  });

  // Collect response times and error rates for usebloom=1
  responseTimesWithBloom.add(responseWithBloom.timings.duration);
  // errorRateWithBloom.add(responseWithBloom.status !== 200);

  if (responseWithBloom.status !== 200 && responseWithBloom.status !== 404) {
    errorRateWithBloom.add(1);
  }


  // Check if the maximum response time threshold is exceeded
  if (responseWithBloom.timings.duration > maxResponseTimeThreshold) {
    console.warn(`Maximum response time threshold (${maxResponseTimeThreshold} ms) exceeded. Adjusting load.`);
    // You can implement logic here to dynamically adjust the load (e.g., increase VUs or RPS)
    // Example: Increase the number of VUs by 10% each time
    __VU += Math.ceil(__VU * 0.1);
  }

  sleep(0.05);
}

export function teardown(data) {
  console.log('Results for usebloom=1:');
  console.log(`- Average Response Time: ${responseTimesWithBloom.mean} ms`);
  console.log(`- Error Rate: ${errorRateWithBloom.count}%\n`);
}
