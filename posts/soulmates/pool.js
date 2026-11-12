// The small example of the post: a pool of 4 people, one of them is your soul mate, and you meet 2.
// Each press plays one life with a random soul mate and two random meetings.
// Over many lives the share that find their soul mate settles near 2/4 = 0.5 when you always
// recognize them, and near 0.5 × 0.5 = 0.25 when you recognize them half of the time.
(function () {
  const root = document.getElementById("pool");
  if (!root) return;
  const dots = Array.from(root.querySelectorAll(".pool-dots i"));
  const says = root.querySelector(".pool-says"), half = root.querySelector("[data-half]");
  const foundOut = root.querySelector("[data-found]"), livesOut = root.querySelector("[data-lives]");
  const still = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  let found = 0, lives = 0, timers = [];

  // One life: who the soul mate is, which two different people you meet, and whether you recognize them.
  function life(halfTheTime) {
    const mate = Math.floor(Math.random() * 4);
    const first = Math.floor(Math.random() * 4);
    const second = (first + 1 + Math.floor(Math.random() * 3)) % 4;
    const met = mate === first || mate === second;
    return { mate, first, second, met, recognized: met && (!halfTheTime || Math.random() < 0.5) };
  }

  function paint(l, step) { // step 1 shows the soul mate, 2 the first meeting, 3 the second
    dots.forEach(function (dot, i) {
      const isMet = (step >= 2 && i === l.first) || (step >= 3 && i === l.second);
      dot.className = (i === l.mate ? "mate" : "") + (isMet ? " met" : "");
    });
  }

  function count(l) {
    lives += 1;
    if (l.recognized) found += 1;
    foundOut.textContent = found;
    livesOut.textContent = lives;
  }

  function verdict(l) {
    if (l.recognized) return "You met your soul mate and recognized them.";
    return l.met ? "You met your soul mate and did not recognize them." : "You never met your soul mate.";
  }

  function playOne() {
    timers.forEach(clearTimeout);
    const l = life(half.checked), gap = still ? 0 : 700;
    paint(l, 1);
    says.textContent = "The ringed dot is your soul mate.";
    timers = [
      setTimeout(function () { paint(l, 2); says.textContent = "You meet one person."; }, gap),
      setTimeout(function () { paint(l, 3); says.textContent = "You meet a second person."; }, 2 * gap),
      setTimeout(function () { says.textContent = verdict(l); count(l); }, 3 * gap),
    ];
  }

  function playMany() {
    timers.forEach(clearTimeout);
    let last;
    for (let i = 0; i < 100; i++) { last = life(half.checked); count(last); }
    paint(last, 3);
    says.textContent = "100 more lives played. The dots show the last one.";
  }

  function reset() { // the two settings are two different experiments, so the tally starts again
    timers.forEach(clearTimeout);
    found = lives = 0;
    foundOut.textContent = livesOut.textContent = 0;
    dots.forEach(function (dot) { dot.className = ""; });
    says.textContent = "Four people. One of them is your soul mate, and you will meet two.";
  }

  root.querySelector("[data-one]").addEventListener("click", playOne);
  root.querySelector("[data-many]").addEventListener("click", playMany);
  half.addEventListener("change", reset);

  // The check: without the recognition step, your soul mate is among the two you meet in half of all lives.
  let hits = 0;
  for (let i = 0; i < 4000; i++) if (life(false).recognized) hits += 1;
  console.assert(Math.abs(hits / 4000 - 0.5) < 0.05, "pool.js: the share should be near 0.5, got " + hits / 4000);
})();
