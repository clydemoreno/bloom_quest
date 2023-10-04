import http from 'k6/http';
import { sleep, check } from 'k6';
import { Trend, Rate } from 'k6/metrics';

// Define the number of VUs using an environment variable
const VUS = __ENV.VUS || 100;

// Define custom metrics for usebloom=0
const responseTimesWithoutBloom = new Trend('response_times_without_bloom');
const errorRateWithoutBloom = new Rate('error_rate_without_bloom');

// Define the maximum acceptable average response time (in milliseconds)
const maxAverageResponseTime = 500; // 500 milliseconds

export const options = {
  stages: [
    { duration: '10s', target: VUS * 0.50 }, // Ramp up to the specified number of VUs over 10 seconds
    { duration: '30s', target: VUS }, // Stay at the specified number of VUs for 1 minute (usebloom=0)
    { duration: '10s', target: 0 },  // Ramp down to 0 VUs over 10 seconds
  ],
};

export default function () {
  // Generate a random order ID based on the distribution
  let randomOrderId;
  const randomValue = Math.random();

  if (randomValue <= 0.05) {
    // 5% of requests with order ID between 1 and 201
    randomOrderId = Math.floor(Math.random() * 201) + 1;
  } else {
    // 95% of requests with order ID between 201 and 10,000
    randomOrderId = Math.floor(Math.random() * 9800) + 201;
  }

  // Test with usebloom=0
  if (__VU <= VUS) {
    const urlWithoutBloom = `http://127.0.0.1:5000/orders/${randomOrderId}?usebloom=0`;
    const responseWithoutBloom = http.get(urlWithoutBloom);
    check(responseWithoutBloom, {
      'is status 200': (r) => r.status === 200,
      'is status 404': (r) => r.status === 404,
      'response time is within threshold': (r) => r.timings.duration <= maxAverageResponseTime,
    });

    // Collect response times and error rates for usebloom=0
    responseTimesWithoutBloom.add(responseWithoutBloom.timings.duration);
    errorRateWithoutBloom.add(responseWithoutBloom.status !== 200);

    // Check if the average response time exceeds the threshold, and stop making requests if it does
    if (responseTimesWithoutBloom.avg > maxAverageResponseTime) {
      console.warn(`Average response time (without bloom) exceeded the threshold (${maxAverageResponseTime} ms). Stopping further requests.`);
      return;
    }

    sleep(0.5);
  }
}

export function teardown(data) {
  console.log('Results for usebloom=0:');
  console.log(`- Average Response Time: ${responseTimesWithoutBloom.mean} ms`);
  console.log(`- Error Rate: ${errorRateWithoutBloom.count}%\n`);
}
