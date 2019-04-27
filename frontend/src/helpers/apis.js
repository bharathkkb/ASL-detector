export const predict = body =>
  fetch('http://34.74.97.21:5000/test/api/predict', {
    method: 'POST',
    body,
  }).then(async res => (await res.json()).id);

export const getPrediction = body =>
  fetch('http://34.74.97.21:5000/test/api/job', {
    method: 'POST',
    body,
  }).then(res => res.json());
