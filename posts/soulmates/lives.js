// 1,000 lives from age 18 to 60. Each dot is one life.
//
// LIT[i] is how many of 1,000 people have had a partner by age 18 + i. The numbers are the
// posterior mean of the partner model in the soulmates repository (notebook 03), computed
// from data/demo_inputs.json. The survey behind the model covers ages 18 to 60.
(function () {
  const LIT = [569, 638, 738, 804, 850, 882, 906, 924, 937, 948, 956, 963, 967, 970, 973, 976, 978, 980, 981,
    983, 984, 985, 986, 987, 988, 988, 989, 990, 990, 991, 991, 991, 992, 992, 992, 992, 993, 993, 993, 993,
    993, 994, 994];
  const FIRST = 18, LAST = FIRST + LIT.length - 1, SECONDS = 8;

  const root = document.getElementById("lives");
  if (!root) return;
  const canvas = root.querySelector("canvas"), ctx = canvas.getContext("2d");
  const slider = root.querySelector("input"), button = root.querySelector("button");
  const ageOut = root.querySelector("[data-age]"), litOut = root.querySelector("[data-lit]");

  // A fixed shuffle, so every reader sees the same dots light up in the same order.
  const rank = Array.from({ length: 1000 }, (_, i) => i);
  let seed = 14;
  for (let i = 999; i > 0; i--) {
    seed = (seed * 16807) % 2147483647;
    const j = seed % (i + 1);
    [rank[i], rank[j]] = [rank[j], rank[i]];
  }

  // The age falls between two birthdays while the animation runs, so the count is interpolated.
  function litAt(age) {
    const i = Math.min(Math.floor(age) - FIRST, LIT.length - 2), part = age - FIRST - i;
    return Math.round(LIT[i] + (LIT[i + 1] - LIT[i]) * part);
  }

  function draw(age) {
    const width = canvas.clientWidth, cols = width < 480 ? 40 : 50, step = width / cols;
    const height = step * (1000 / cols), scale = window.devicePixelRatio || 1;
    canvas.style.height = height + "px";
    canvas.width = Math.round(width * scale);
    canvas.height = Math.round(height * scale);
    ctx.setTransform(scale, 0, 0, scale, 0, 0);
    // The colours come from the page: the sleeve colour of the post and its ink.
    const css = getComputedStyle(root), on = css.getPropertyValue("--s1"), off = css.color, lit = litAt(age);
    for (let i = 0; i < 1000; i++) {
      const isLit = rank[i] < lit;
      ctx.fillStyle = isLit ? on : off;
      ctx.globalAlpha = isLit ? 1 : 0.14;
      ctx.beginPath();
      ctx.arc((i % cols + 0.5) * step, (Math.floor(i / cols) + 0.5) * step, step * 0.33, 0, 2 * Math.PI);
      ctx.fill();
    }
    ageOut.textContent = slider.value = Math.floor(age);
    litOut.textContent = lit;
  }

  let frame = null;
  function play() {
    cancelAnimationFrame(frame);
    const start = performance.now();
    (function tick(now) {
      const done = Math.min((now - start) / (SECONDS * 1000), 1);
      // Squared, so the early years run slowly. Most dots light up before 30.
      draw(FIRST + (LAST - FIRST) * done * done);
      if (done < 1) frame = requestAnimationFrame(tick);
    })(start);
  }

  button.addEventListener("click", play);
  slider.addEventListener("input", function () { cancelAnimationFrame(frame); draw(+slider.value); });
  window.addEventListener("resize", function () { draw(+slider.value); });
  // Readers who switched motion off keep the slider and lose the play button.
  if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) button.hidden = true;

  // The check: these three counts are the ones the post states in its text.
  console.assert(litAt(18) === 569 && litAt(30) === 967 && litAt(60) === 994, "lives.js: counts differ from the post");
  draw(FIRST);
})();
