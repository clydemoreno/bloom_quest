import http from 'k6/http';
import { sleep, check } from 'k6';

// Define the number of VUs using an environment variable
const VUS = __ENV.VUS || 10;

export const options = {
  stages: [
    { duration: '10s', target: VUS }, // Ramp up to the specified number of VUs over 30 seconds
    { duration: '1m', target: VUS }, // Stay at the specified number of VUs for 2 minutes (usebloom=1)
    { duration: '1m', target: VUS }, // Stay at the specified number of VUs for 2 minutes (usebloom=0)
    { duration: '10s', target: 0 },  // Ramp down to 0 VUs over 30 seconds
  ],
//   thresholds: {
//     http_req_duration: ['p(95)<500'], // Set a response time threshold
//   },
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
    sleep(0.5);
  }

  // Test with usebloom=0
  if (__VU <= VUS) {
    const urlWithoutBloom = `http://127.0.0.1:5000/orders/${randomOrderId}?usebloom=0`;
    const responseWithoutBloom = http.get(urlWithoutBloom);
    check(responseWithoutBloom, {
      'is status 200': (r) => r.status === 200,
      'is status 404': (r) => r.status === 404,
    });
    sleep(0.5);
  }
}
