import http from 'k6/http';
import { sleep, check } from 'k6';

export default function () {
  // Generate a random number to decide if it's below 201 or above
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

  // Make an HTTP GET request with the random order ID
  const url = `http://127.0.0.1:5000/orders/${randomOrderId}?usesbloom=1`;
  const response = http.get(url);

  // Check the response status code
  check(response, {
    'is status 200': (r) => r.status === 200,
    'is status 404': (r) => r.status === 404,
  });

  sleep(0.5); // 0.5-second pause between requests
}
