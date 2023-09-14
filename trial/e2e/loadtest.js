import http from 'k6/http';
import { sleep, check } from 'k6';
import { Trend, Rate } from 'k6/metrics'; // Import Rate from k6/metrics

// Define the number of VUs using an environment variable
const VUS = __ENV.VUS || 10;

// Define custom metrics
const responseTimesWithBloom = new Trend('response_times_with_bloom');
const responseTimesWithoutBloom = new Trend('response_times_without_bloom');
const errorRateWithBloom = new Rate('error_rate_with_bloom');
const errorRateWithoutBloom = new Rate('error_rate_without_bloom');

export const options = {
  stages: [
    { duration: '10s', target: VUS * 0.50 }, // Ramp up to the specified number of VUs over 10 seconds
    { duration: '30s', target: VUS }, // Stay at the specified number of VUs for 1 minute (usebloom=1)
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

  // Test with usebloom=1
  if (__VU <= VUS) {
    const urlWithBloom = `http://127.0.0.1:5000/orders/${randomOrderId}?usebloom=1`;
    const responseWithBloom = http.get(urlWithBloom);
    check(responseWithBloom, {
      'is status 200': (r) => r.status === 200,
      'is status 404': (r) => r.status === 404,
    });


    // Collect response times and error rates for usebloom=1
    responseTimesWithBloom.add(responseWithBloom.timings.duration);
    errorRateWithBloom.add(responseWithBloom.status !== 200);    

    sleep(0.05);
  }

  // Test with usebloom=0
  if (__VU <= VUS) {
    const urlWithoutBloom = `http://127.0.0.1:5000/orders/${randomOrderId}?usebloom=0`;
    const responseWithoutBloom = http.get(urlWithoutBloom);
    check(responseWithoutBloom, {
      'is status 200': (r) => r.status === 200,
      'is status 404': (r) => r.status === 404,
    });

    // Collect response times and error rates
    responseTimesWithoutBloom.add(responseWithoutBloom.timings.duration);
    errorRateWithoutBloom.add(responseWithoutBloom.status !== 200);

    sleep(0.5);
  }
}

export function teardown(data) {
  console.log('Results for usebloom=1:');
  console.log(`- Average Response Time: ${responseTimesWithBloom.mean} ms`);
  console.log(`- Error Rate: ${errorRateWithBloom.count}%\n`);

  console.log('Results for usebloom=0:');
  console.log(`- Average Response Time: ${responseTimesWithoutBloom.mean} ms`);
  console.log(`- Error Rate: ${errorRateWithoutBloom.count}%\n`);
}
