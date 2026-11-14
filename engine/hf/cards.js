/* Era das Feras — animation of every card on one paused GSAP timeline (HyperFrames contract: seek-safe tweens only). */
(function () {
  var tl = gsap.timeline({ paused: true });
  var CARDS = window.CARDS || [];
  function q(el, s) { return el.querySelectorAll(s); }
  function q1(el, s) { return el.querySelector(s); }

  // shared layers: slow camera move on the picture, film grain jitter, one light leak pass
  function common(el, c, t0, d) {
    var img = q1(el, ".bg img");
    if (img) {
      var mv = c.move || "push";
      var from = { push: { scale: 1.16 }, pull: { scale: 1.0 }, left: { scale: 1.14, xPercent: 3 }, right: { scale: 1.14, xPercent: -3 },
                   up: { scale: 1.14, yPercent: 3 } }[mv] || { scale: 1.16 };
      var to = { push: { scale: 1.02 }, pull: { scale: 1.16 }, left: { scale: 1.14, xPercent: -3 }, right: { scale: 1.14, xPercent: 3 },
                 up: { scale: 1.14, yPercent: -3 } }[mv] || { scale: 1.02 };
      tl.fromTo(img, from, Object.assign({ duration: d, ease: "none" }, to), t0);
      if (c.blurin) tl.fromTo(img, { filter: "blur(18px) brightness(.6)" }, { filter: "blur(0px) brightness(1)", duration: 1.1, ease: "power2.out" }, t0);
    }
    var g = q1(el, ".grain");
    if (g) {   // stepped jitter, 12 positions per second
      var n = Math.max(1, Math.floor(d * 12));
      for (var i = 0; i < n; i++) tl.set(g, { x: ((i * 37) % 60) - 30, y: ((i * 53) % 60) - 30 }, t0 + i / 12);
    }
    var lk = q1(el, ".leak");
    if (lk && c.leak !== false) {
      tl.fromTo(lk, { x: 0, opacity: 0 }, { x: 2900, opacity: 1, duration: 1.6, ease: "power1.inOut" }, t0 + 0.05);
      tl.to(lk, { opacity: 0, duration: 0.4 }, t0 + 1.3);
    }
  }

  function words(el, sel, t0, stag) {
    tl.from(q(el, sel), { yPercent: 115, duration: 0.7, ease: "power3.out", stagger: stag || 0.07 }, t0);
  }

  var A = {
    titulo: function (el, c, t0, d) {
      tl.from(q1(el, ".kick"), { opacity: 0, x: -40, duration: 0.9, ease: "power3.out" }, t0 + 0.3);
      words(el, "h1 .mask > span", t0 + 0.55, 0.09);
      tl.from(q1(el, ".rule"), { scaleX: 0, duration: 0.8, ease: "power4.out" }, t0 + 1.2);
      tl.from(q1(el, ".sub"), { opacity: 0, y: 20, duration: 0.6, ease: "power2.out" }, t0 + 1.5);
    },
    capitulo: function (el, c, t0, d) {
      tl.from(q1(el, ".num"), { opacity: 0, x: -120, duration: 1.2, ease: "power3.out" }, t0 + 0.1);
      tl.to(q1(el, ".num"), { x: 40, duration: d, ease: "none" }, t0 + 1.3);
      tl.from(q1(el, ".kick"), { opacity: 0, x: -30, duration: 0.6, ease: "power2.out" }, t0 + 0.35);
      words(el, "h2 .mask > span", t0 + 0.5, 0.08);
      tl.from(q1(el, ".rule"), { scaleX: 0, duration: 0.9, ease: "power4.out" }, t0 + 1.0);
    },
    rotulo: function (el, c, t0, d) {
      var r = q1(el, ".lt").classList.contains("r");
      tl.from(q1(el, ".tag"), { opacity: 0, x: r ? 40 : -40, duration: 0.5, ease: "back.out(2)" }, t0 + 0.35);
      words(el, ".name .mask > span", t0 + 0.5, 0.06);
      tl.from(q1(el, ".rule"), { scaleX: 0, duration: 0.7, ease: "power4.out" }, t0 + 0.8);
      if (q1(el, ".sci")) tl.from(q1(el, ".sci"), { opacity: 0, y: 12, duration: 0.5 }, t0 + 1.0);
    },
    ficha: function (el, c, t0, d) {
      tl.from(q1(el, ".panel"), { xPercent: 100, duration: 0.8, ease: "power4.out" }, t0 + 0.1);
      tl.from(q1(el, ".kick"), { opacity: 0, duration: 0.4 }, t0 + 0.6);
      words(el, "h3 .mask > span", t0 + 0.65, 0.06);
      tl.from(q1(el, ".sci"), { opacity: 0, duration: 0.5 }, t0 + 0.9);
      tl.from(q(el, ".row"), { opacity: 0, x: 60, duration: 0.5, ease: "power3.out", stagger: 0.35 }, t0 + 1.1);
      if (q1(el, ".src")) tl.from(q1(el, ".src"), { opacity: 0, duration: 0.5 }, t0 + 1.6);
    },
    numero: function (el, c, t0, d) {
      var v = q1(el, ".val"), o = { n: c.from || 0 }, to = c.value, dec = c.decimals || 0;
      function fmt(x) { return x.toLocaleString("pt-BR", { minimumFractionDigits: dec, maximumFractionDigits: dec }); }
      v.textContent = fmt(o.n);
      tl.from(v, { opacity: 0, scale: 0.85, duration: 0.5, ease: "power2.out" }, t0 + 0.2);
      tl.to(o, { n: to, duration: Math.min(2.2, d * 0.5), ease: "power3.out", onUpdate: function () { v.textContent = fmt(o.n); } }, t0 + 0.3);
      tl.set(v, { textContent: fmt(to) }, t0 + 0.3 + Math.min(2.2, d * 0.5));
      tl.from(q1(el, ".unit"), { opacity: 0, y: 20, duration: 0.5 }, t0 + 0.8);
      tl.from(q1(el, ".rule"), { scaleX: 0, duration: 0.7, ease: "power4.out" }, t0 + 1.2);
      tl.from(q1(el, ".lab"), { opacity: 0, duration: 0.6 }, t0 + 1.5);
    },
    mapa: function (el, c, t0, d) {
      var paths = q(el, "path.st"), hl = q1(el, "path.hl"), stage = q1(el, ".stage");
      paths.forEach(function (p) { var L = parseFloat(p.getAttribute("data-len")); p.style.strokeDasharray = L; p.style.strokeDashoffset = L; });
      tl.to(paths, { strokeDashoffset: 0, duration: 1.4, ease: "power2.inOut", stagger: 0.02 }, t0 + 0.1);
      tl.from(q(el, "path.st"), { fillOpacity: 0, duration: 0.8 }, t0 + 1.0);
      var L = c.hlLen || 900; hl.style.strokeDasharray = L; hl.style.strokeDashoffset = L;
      tl.to(hl, { strokeDashoffset: 0, duration: 0.8, ease: "power2.out" }, t0 + 1.4);
      tl.to(hl, { fillOpacity: 0.85, duration: 0.6 }, t0 + 1.9);
      var bb = c.bb, k = c.k;   // highlighted state's bbox in map units, map units -> px (computed by hf_cards.py)
      var ox = (bb[0] + bb[2]) / 2 * k, oy = (bb[1] + bb[3]) / 2 * k;
      stage.style.transformOrigin = ox + "px " + oy + "px";
      tl.to(stage, { scale: c.zoom || 2.4, x: 640 - (260 + ox), y: 560 - (50 + oy), duration: 2.0, ease: "power3.inOut" }, t0 + 2.0);
      tl.from(q1(el, ".pin"), { scale: 0, opacity: 0, duration: 0.45, ease: "back.out(3)" }, t0 + 3.6);
      q(el, ".ring").forEach(function (r, i) {
        for (var k = 0; k < 3; k++) tl.fromTo(r, { scale: 1, opacity: 0.9 }, { scale: 5, opacity: 0, duration: 1.4, ease: "power2.out" }, t0 + 3.8 + i * 0.45 + k * 1.4);
      });
      tl.from(q1(el, ".info .kick"), { opacity: 0, x: 30, duration: 0.5 }, t0 + 3.9);
      words(el, ".info h3 .mask > span", t0 + 4.0, 0.06);
      tl.from(q1(el, ".info .sub"), { opacity: 0, y: 16, duration: 0.6 }, t0 + 4.4);
      tl.from(q1(el, ".info .rule"), { scaleX: 0, duration: 0.7, ease: "power4.out" }, t0 + 4.6);
    },
    linha: function (el, c, t0, d) {
      tl.from(q1(el, ".ttl .kick"), { opacity: 0, duration: 0.5 }, t0 + 0.2);
      words(el, ".ttl h3 .mask > span", t0 + 0.3, 0.06);
      tl.from(q(el, ".era"), { scaleX: 0, duration: 0.6, ease: "power3.out", stagger: 0.25 }, t0 + 0.6);
      tl.from(q(el, ".tick"), { opacity: 0, y: 10, duration: 0.4, stagger: 0.15 }, t0 + 1.2);
      tl.from(q1(el, ".mark"), { scaleY: 0, duration: 0.6, ease: "back.out(2)" }, t0 + 2.0);
      tl.from(q1(el, ".mlab"), { opacity: 0, y: 30, duration: 0.6, ease: "power3.out" }, t0 + 2.3);
    },
    comparar: function (el, c, t0, d) {
      var r = q1(el, ".half.r");
      tl.fromTo(r, { clipPath: "inset(0 0 0 100%)" }, { clipPath: "inset(0 0 0 50%)", duration: 1.2, ease: "power3.inOut" }, t0 + 1.0);
      tl.fromTo(q1(el, ".div"), { x: 960 }, { x: 0, duration: 1.2, ease: "power3.inOut" }, t0 + 1.0);
      tl.fromTo(q(el, ".half img"), { scale: 1.12 }, { scale: 1.0, duration: d, ease: "none" }, t0);
      tl.from(q1(el, ".lab.l"), { opacity: 0, y: 20, duration: 0.5 }, t0 + 0.3);
      tl.from(q1(el, ".lab.r"), { opacity: 0, y: 20, duration: 0.5 }, t0 + 1.9);
    },
    frase: function (el, c, t0, d) {
      var ws = q(el, "p .w");
      tl.from(ws, { opacity: 0, scale: 1.5, filter: "blur(10px)", duration: 0.45, ease: "power3.out", stagger: Math.min(0.16, 1.4 / ws.length) }, t0 + 0.2);
      var em = q1(el, "p .em");
      if (em) {
        var te = t0 + 0.2 + Array.prototype.indexOf.call(ws, em) * Math.min(0.16, 1.4 / ws.length) + 0.4;
        tl.to(q1(el, "p"), { x: 8, duration: 0.033 }, te).to(q1(el, "p"), { x: -6, duration: 0.033 }).to(q1(el, "p"), { x: 0, duration: 0.033 });
      }
    },
    escala: function (el, c, t0, d) {
      tl.from(q1(el, ".ttl .kick"), { opacity: 0, duration: 0.5 }, t0 + 0.2);
      words(el, ".ttl h3 .mask > span", t0 + 0.3, 0.06);
      q(el, ".row").forEach(function (r, i) {
        var t = t0 + 0.9 + i * 0.55;
        tl.from(q1(r, ".n"), { opacity: 0, x: -30, duration: 0.4 }, t);
        tl.from(q1(r, ".b"), { scaleX: 0, duration: 0.9, ease: "power3.out" }, t + 0.1);
        tl.from(q1(r, ".v"), { opacity: 0, duration: 0.4 }, t + 0.7);
      });
    },
    perguntas: function (el, c, t0, d) {
      var qs = q(el, ".q"), step = Math.max(0.6, (d - 1.0) / Math.max(1, qs.length));
      qs.forEach(function (x, i) {
        var t = t0 + 0.3 + (c.at ? c.at[i] : i * step);
        tl.from(q1(x, ".i"), { opacity: 0, x: -40, duration: 0.45, ease: "power3.out" }, t);
        tl.from(q(x, ".t .mask > span"), { yPercent: 115, duration: 0.6, ease: "power3.out", stagger: 0.04 }, t + 0.1);
      });
    },
    cta: function (el, c, t0, d) {
      words(el, "h3 .mask > span", t0 + 0.3, 0.07);
      tl.from(q1(el, ".btn"), { scale: 0, opacity: 0, duration: 0.6, ease: "back.out(2.2)" }, t0 + 1.1);
      var b = q1(el, ".bell");
      for (var k = 0; k < 2; k++) tl.to(b, { rotation: 18, duration: 0.08 }, t0 + 1.9 + k * 1.6).to(b, { rotation: -16, duration: 0.1 }).to(b, { rotation: 10, duration: 0.1 }).to(b, { rotation: 0, duration: 0.12 });
      tl.from(q1(el, ".sub"), { opacity: 0, y: 16, duration: 0.6 }, t0 + 1.6);
    }
  };

  // time each layout needs to finish its reveal; a shorter card plays its reveal faster (never slower)
  var NATURAL = { titulo: 2.2, capitulo: 1.9, rotulo: 1.5, ficha: 2.7, numero: 2.2, mapa: 5.0, linha: 2.9, comparar: 2.4,
                  frase: 1.6, escala: 3.6, perguntas: 3.0, cta: 2.3 };
  var master = tl;
  CARDS.forEach(function (c, i) {
    var el = document.getElementById("c" + i);
    common(el, c, c.start, c.dur);
    tl = gsap.timeline();
    (A[c.kind] || function () {})(el, c, 0, c.dur);
    var need = NATURAL[c.kind] || 2, k = Math.min(1, Math.max(0.35, (c.dur - 1.6) / need));
    tl.timeScale(1 / k);
    var sub = tl; tl = master;
    tl.add(sub, c.start);
  });
  window.__timelines = window.__timelines || {};
  window.__timelines["root"] = tl;
})();
