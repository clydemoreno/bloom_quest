import http from 'k6/http';
import { sleep, check } from 'k6';

export const options = {
  stages: [
    { duration: '30s', target: 10 }, // Ramp up to 10 VUs over 30 seconds
    { duration: '1m', target: 10 },  // Stay at 10 VUs for 1 minute
    { duration: '30s', target: 100 }, // Ramp up to 100 VUs over 30 seconds
    { duration: '1m', target: 100 },  // Stay at 100 VUs for 1 minute
    { duration: '30s', target: 0 },   // Ramp down to 0 VUs over 30 seconds
  ],
  thresholds: {
    http_req_duration: ['p(95)<500'], // Set a response time threshold
  },
};

export default function () {
  // Your script logic here

  const randomValue = Math.random();

  // Generate a random order ID based on the distribution
  let randomOrderId;
  if (randomValue <= 0.05) {
    // 5% of requests with order ID between 1 and 201
    randomOrderId = Math.floor(Math.random() * 201) + 1;
  } else {
    // 95% of requests with order ID between 201 and 10,000
    randomOrderId = Math.floor(Math.random() * 9800) + 201;
  }



//   const randomOrderId = Math.floor(Math.random() * 9800) + 201;
  const url = `http://127.0.0.1:5000/orders/${randomOrderId}?usebloom=0`;
  const response = http.get(url);
  check(response, {
    'is status 200': (r) => r.status === 200,
    'is status 404': (r) => r.status === 404,
  });
  sleep(0.5);
}


