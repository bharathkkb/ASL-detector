export const predict = body =>
  fetch(`${process.env.DOMAIN || ''}/test/api/predict`, {
    method: 'POST',
    body,
  }).then(async res => (await res.json()).id);

export const getPrediction = body =>
  fetch(`${process.env.DOMAIN || ''}/test/api/job`, {
    method: 'POST',
    body,
  }).then(res => res.json());
