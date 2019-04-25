export const predict = body =>
  fetch('http://localhost:5000/test/api/predict', {
    method: 'POST',
    body,
  }).then(async res => (await res.json()).id);

export const getPrediction = body =>
  fetch('http://localhost:5000/test/api/job', {
    method: 'POST',
    body,
  }).then(res => res.json());
