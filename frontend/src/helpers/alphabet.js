const ALPHABET = [
  'A',
  'B',
  'C',
  'D',
  'E',
  'F',
  'G',
  'H',
  'I',
  'J',
  'K',
  'L',
  'M',
  'N',
  'O',
  'P',
  'Q',
  'R',
  'S',
  'T',
  'U',
  'V',
  'W',
  'X',
  'Y',
  'Z',
  'del',
  'nothing',
  'space',
];

export const getAlphabet = ({ predictions: [results] }) => {
  const [index] = results.map((v, i) => i).filter(i => results[i] === 1);
  return ALPHABET[index];
};
