import http from 'k6/http';
import { sleep } from 'k6';

export default function () {
  http.get('http://127.0.0.1:5000/orders/201');
  sleep(0.5); // 1-second pause between requests
}
