function seededRandom(seed) {
  let value = Number(seed) % 2147483647;
  if (value <= 0) {
    value += 2147483646;
  }
  return function () {
    value =
      (value * 16807) %
      2147483647;
    return (
      (value - 1) /
      2147483646
    );
  };
}


function gaussianRandom(random) {
  let u = 0;
  let v = 0;
  while (u === 0) {
    u = random();
  }
  while (v === 0) {
    v = random();
  }
  return (
    Math.sqrt(
      -2 *
        Math.log(u)
    ) *
    Math.cos(
      2 *
        Math.PI *
        v
    )
  );
}


export function generateQueryVector(dimension,seed) {
  const random =
    seededRandom(seed);

  return Array.from(
    { length: dimension },
    () =>
      gaussianRandom(random)
  );
}