export const predict = body =>
  fetch('/test/api/predict', {
    method: 'POST',
    body,
  }).then(async res => (await res.json()).id);

export const getPrediction = body =>
  fetch('/test/api/job', {
    method: 'POST',
    body,
  }).then(res => res.json());
