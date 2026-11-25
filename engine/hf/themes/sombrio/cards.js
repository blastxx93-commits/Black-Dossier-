/* Era das Feras — tema "Gelo": animações (GSAP, timeline pausada, seek-safe). */
(function () {
  var tl = gsap.timeline({ paused: true });
  var CARDS = window.CARDS || [];
  function q(el, s) { return el.querySelectorAll(s); }
  function q1(el, s) { return el.querySelector(s); }
  function rnd(i) { var x = Math.sin(i * 12.9898) * 43758.5453; return x - Math.floor(x); }

  // shared layers: camera on the picture (push + slight 3D drift), snow, cold light sweep, grain jitter
  function common(el, c, t0, d) {
    q(el, ".bg img, .pane img").forEach(function (img, k) {
      var mv = c.move || ["push", "drift", "pull", "rise"][(c.i + k) % 4];
      var A = { push: [{ scale: 1.18, x: 0 }, { scale: 1.04, x: 0 }], pull: [{ scale: 1.04 }, { scale: 1.18 }],
                drift: [{ scale: 1.14, xPercent: -2.5 }, { scale: 1.1, xPercent: 2.5 }], rise: [{ scale: 1.14, yPercent: 2.5 }, { scale: 1.1, yPercent: -2 }] }[mv];
      tl.fromTo(img, A[0], Object.assign({ duration: d, ease: "sine.inOut" }, A[1]), t0);
      if (c.blurin) tl.fromTo(img, { filter: "blur(16px) brightness(.5)" }, { filter: "blur(0px) brightness(1)", duration: 1.2, ease: "power2.out" }, t0);
    });
    q(el, ".snow i").forEach(function (f, k) {
      var sp = 0.5 + rnd(k + c.i * 7) * 1.2, x0 = rnd(k * 3 + 1) * 1920, y0 = -40 - rnd(k * 5 + 2) * 1080;
      tl.fromTo(f, { x: x0, y: y0 }, { x: x0 + (rnd(k) - 0.5) * 220, y: y0 + 1300 * sp * Math.max(1, d / 4), duration: d, ease: "none" }, t0);
    });
    var sw = q1(el, ".sweep");
    if (sw) tl.fromTo(sw, { x: 0 }, { x: 3200, duration: Math.min(2.4, d), ease: "power1.inOut" }, t0 + 0.2);
    var g = q1(el, ".grain");
    if (g) { var n = Math.max(1, Math.floor(d * 12)); for (var i = 0; i < n; i++) tl.set(g, { x: ((i * 37) % 60) - 30, y: ((i * 53) % 60) - 30 }, t0 + i / 12); }
  }

  function rise(el, sel, t0, stag) { tl.from(q(el, sel), { yPercent: 110, duration: 0.65, ease: "power4.out", stagger: stag || 0.06 }, t0); }

  var A = {
    caso: function (el, c, t0, d) {
      tl.fromTo(q1(el, ".num"), { opacity: 0, scale: 1.3 }, { opacity: 1, scale: 1, duration: 0.6, ease: "power3.out" }, t0 + 0.1);
      tl.to(q1(el, ".num"), { opacity: 0.4, duration: 0.05 }, t0 + 0.75).to(q1(el, ".num"), { opacity: 1, duration: 0.05 }).to(q1(el, ".num"), { opacity: 0.5, duration: 0.04 }).to(q1(el, ".num"), { opacity: 1, duration: 0.05 });
      tl.from(q1(el, ".lab"), { opacity: 0, x: -30, duration: 0.45 }, t0 + 0.35);
      rise(el, "h2 .mask > span", t0 + 0.5, 0.07);
      tl.from(q(el, ".meta span"), { opacity: 0, y: 14, duration: 0.45, stagger: 0.2 }, t0 + 1.0);
    },
    titulo: function (el, c, t0, d) {
      tl.from(q1(el, ".chip"), { xPercent: -110, opacity: 0, duration: 0.5, ease: "power3.out" }, t0 + 0.3);
      rise(el, "h1 .mask > span", t0 + 0.5, 0.08);
      tl.from(q1(el, ".line"), { scaleX: 0, duration: 0.8, ease: "power4.out" }, t0 + 1.1);
      tl.from(q1(el, ".sub"), { opacity: 0, y: 24, duration: 0.6 }, t0 + 1.4);
    },
    rodada: function (el, c, t0, d) {
      tl.fromTo(q1(el, ".pane"), { clipPath: "polygon(100% 0, 100% 0, 100% 100%, 100% 100%)" }, { clipPath: "polygon(22% 0, 100% 0, 100% 100%, 0% 100%)", duration: 0.9, ease: "power4.inOut" }, t0 + 0.1);
      tl.from(q1(el, ".num"), { x: -80, opacity: 0, duration: 0.7, ease: "power3.out" }, t0);
      tl.fromTo(q1(el, ".num .fill"), { clipPath: "inset(100% 0 0 0)" }, { clipPath: "inset(0% 0 0 0)", duration: 0.9, ease: "power2.inOut" }, t0 + 0.5);
      tl.from(q1(el, ".lab"), { opacity: 0, x: -30, duration: 0.5 }, t0 + 0.6);
      rise(el, "h2 .mask > span", t0 + 0.75, 0.07);
      tl.from(q1(el, ".chip"), { opacity: 0, y: 16, duration: 0.5 }, t0 + 1.1);
      tl.from(q1(el, ".era"), { opacity: 0, duration: 0.6 }, t0 + 1.3);
      tl.from(q(el, ".pips b"), { scaleX: 0, duration: 0.3, stagger: 0.06 }, t0 + 1.0);
    },
    versus: function (el, c, t0, d) {
      tl.from(q1(el, ".pane.l"), { xPercent: -100, duration: 0.7, ease: "power4.out" }, t0);
      tl.from(q1(el, ".pane.r"), { xPercent: 100, duration: 0.7, ease: "power4.out" }, t0 + 0.08);
      tl.from(q1(el, ".seam"), { scaleY: 0, duration: 0.5, ease: "power3.out" }, t0 + 0.5);
      tl.fromTo(q1(el, ".vs"), { scale: 2.6, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.35, ease: "power4.in" }, t0 + 0.7);
      tl.to(q1(el, ".vs"), { x: 9, duration: 0.03 }, t0 + 1.05).to(q1(el, ".vs"), { x: -7, duration: 0.03 }).to(q1(el, ".vs"), { x: 0, duration: 0.03 });
      ["l", "r"].forEach(function (s, k) {
        var sd = q1(el, ".side." + s);
        tl.from(q1(sd, ".chip"), { opacity: 0, y: 14, duration: 0.4 }, t0 + 1.1 + k * 0.15);
        rise(sd, "h3 .mask > span", t0 + 1.2 + k * 0.15, 0.05);
        tl.from(q(sd, ".stat"), { opacity: 0, duration: 0.3, stagger: 0.25 }, t0 + 1.6 + k * 0.15);
        tl.from(q(sd, ".bar"), { scaleX: 0, duration: 0.8, ease: "power3.out", stagger: 0.25 }, t0 + 1.65 + k * 0.15);
      });
    },
    veredito: function (el, c, t0, d) {
      tl.fromTo(q1(el, ".bg img"), { filter: "grayscale(0) contrast(1)" }, { filter: "grayscale(1) contrast(1.15)", duration: 0.8, ease: "power2.inOut" }, t0 + 0.4);
      tl.fromTo(q1(el, ".flash"), { opacity: 0 }, { opacity: 0.85, duration: 0.05 }, t0 + 1.0).to(q1(el, ".flash"), { opacity: 0, duration: 0.35 });
      tl.fromTo(q1(el, ".stamp"), { scale: 2.4, opacity: 0 }, { scale: 1, opacity: 1, duration: 0.28, ease: "power4.in" }, t0 + 0.8);
      tl.to(q1(el, ".stamp"), { x: 8, duration: 0.03 }, t0 + 1.08).to(q1(el, ".stamp"), { x: -6, duration: 0.03 }).to(q1(el, ".stamp"), { x: 0, duration: 0.03 });
    },
    placar: function (el, c, t0, d) {
      tl.from(q(el, ".who"), { opacity: 0, y: -30, duration: 0.5, stagger: 0.12 }, t0 + 0.2);
      tl.from(q1(el, ".mid"), { opacity: 0, duration: 0.4 }, t0 + 0.4);
      q(el, ".digit").forEach(function (dg, k) {
        var o = q1(dg, ".o"), n = q1(dg, ".n");
        if (o.textContent !== n.textContent) {
          tl.set(n, { yPercent: 100 }, t0);
          tl.to(o, { yPercent: -100, duration: 0.45, ease: "power3.in" }, t0 + 1.1 + k * 0.1);
          tl.to(n, { yPercent: 0, duration: 0.5, ease: "back.out(1.6)" }, t0 + 1.4 + k * 0.1);
        } else tl.set(n, { opacity: 0 }, t0);
      });
      tl.from(q1(el, ".sub"), { opacity: 0, y: 16, duration: 0.5 }, t0 + 1.9);
    },
    ficha: function (el, c, t0, d) {
      tl.from(q1(el, ".panel"), { x: 120, opacity: 0, duration: 0.7, ease: "power4.out" }, t0 + 0.15);
      tl.from(q1(el, ".chip"), { opacity: 0, duration: 0.4 }, t0 + 0.5);
      rise(el, "h3 .mask > span", t0 + 0.6, 0.05);
      tl.from(q1(el, ".sci"), { opacity: 0, duration: 0.5 }, t0 + 0.9);
      tl.from(q(el, ".row"), { opacity: 0, x: 50, duration: 0.45, ease: "power3.out", stagger: 0.32 }, t0 + 1.1);
    },
    rotulo: function (el, c, t0, d) {
      var r = q1(el, ".lt").classList.contains("r");
      tl.from(q1(el, ".chip"), { opacity: 0, x: r ? 40 : -40, duration: 0.45, ease: "power3.out" }, t0 + 0.35);
      rise(el, ".name .mask > span", t0 + 0.45, 0.05);
      tl.from(q1(el, ".line"), { scaleX: 0, duration: 0.7, ease: "power4.out" }, t0 + 0.75);
      if (q1(el, ".sci")) tl.from(q1(el, ".sci"), { opacity: 0, y: 10, duration: 0.5 }, t0 + 0.95);
    },
    frase: function (el, c, t0, d) {
      var ws = q(el, "p .w"), st = Math.min(0.14, 1.2 / ws.length);
      tl.from(ws, { opacity: 0, y: 60, scale: 1.25, duration: 0.45, ease: "power4.out", stagger: st }, t0 + 0.2);
      var em = q1(el, "p .em");
      if (em) tl.fromTo(em, { textShadow: "0 0 0px rgba(124,200,242,0)" }, { textShadow: "0 0 30px rgba(179,20,27,.9)", duration: 0.6 }, t0 + 0.3 + ws.length * st);
    },
    escala: function (el, c, t0, d) {
      tl.from(q1(el, ".ttl .chip"), { opacity: 0, duration: 0.4 }, t0 + 0.2);
      rise(el, ".ttl h3 .mask > span", t0 + 0.3, 0.05);
      tl.from(q1(el, ".floor"), { scaleX: 0, duration: 0.6, ease: "power3.out" }, t0 + 0.5);
      q(el, ".c").forEach(function (cc, i) {
        var t = t0 + 0.8 + i * 0.45;
        tl.from(q1(cc, ".b"), { scaleY: 0, duration: 0.9, ease: "power3.out" }, t);
        tl.from(q1(cc, ".v"), { opacity: 0, y: 20, duration: 0.4 }, t + 0.6);
        tl.from(q1(cc, ".n"), { opacity: 0, duration: 0.4 }, t + 0.3);
      });
    },
    mapa: function (el, c, t0, d) {
      var st = q1(el, ".stage");
      tl.from(q(el, "path"), { opacity: 0, duration: 0.8, stagger: { amount: 0.6, from: "random" } }, t0 + 0.05);
      st.style.transformOrigin = c.px + "px " + c.py + "px";
      tl.fromTo(st, { scale: 1, x: 0, y: 0 }, { scale: c.zoom || 2.6, x: 960 - c.px, y: 470 - c.py, duration: 2.2, ease: "power3.inOut" }, t0 + 0.8);
      tl.from(q1(el, ".pin"), { scale: 0, opacity: 0, duration: 0.4, ease: "back.out(3)" }, t0 + 2.6);
      q(el, ".ring").forEach(function (r, i) {
        for (var k = 0; k < 3; k++) tl.fromTo(r, { scale: 1, opacity: 0.9 }, { scale: 5, opacity: 0, duration: 1.3, ease: "power2.out" }, t0 + 2.8 + i * 0.4 + k * 1.3);
      });
      tl.from(q1(el, ".info .chip"), { opacity: 0, x: -30, duration: 0.45 }, t0 + 2.9);
      rise(el, ".info h3 .mask > span", t0 + 3.0, 0.05);
      tl.from(q1(el, ".info .sub"), { opacity: 0, y: 14, duration: 0.5 }, t0 + 3.3);
    },
    perguntas: function (el, c, t0, d) {
      var qs = q(el, ".q"), step = Math.max(0.6, (d - 1.0) / Math.max(1, qs.length));
      qs.forEach(function (x, i) {
        var t = t0 + 0.3 + i * step;
        tl.from(q1(x, ".i"), { opacity: 0, x: -40, duration: 0.4, ease: "power3.out" }, t);
        tl.from(q(x, ".t .mask > span"), { yPercent: 110, duration: 0.55, ease: "power4.out", stagger: 0.04 }, t + 0.1);
      });
    },
    cta: function (el, c, t0, d) {
      rise(el, "h3 .mask > span", t0 + 0.3, 0.07);
      tl.from(q1(el, ".btn"), { scale: 0, opacity: 0, duration: 0.55, ease: "back.out(2.2)" }, t0 + 1.0);
      var b = q1(el, ".bell");
      for (var k = 0; k < 2; k++) tl.to(b, { rotation: 18, duration: 0.08 }, t0 + 1.8 + k * 1.6).to(b, { rotation: -16, duration: 0.1 }).to(b, { rotation: 10, duration: 0.1 }).to(b, { rotation: 0, duration: 0.12 });
      tl.from(q1(el, ".sub"), { opacity: 0, y: 16, duration: 0.6 }, t0 + 1.5);
    }
  };

  var NATURAL = { caso: 1.8, titulo: 2.1, rodada: 1.9, versus: 2.6, veredito: 1.4, placar: 2.4, ficha: 2.6, rotulo: 1.5, frase: 1.6, escala: 3.4,
                  mapa: 3.8, perguntas: 3.0, cta: 2.3 };
  var master = tl;
  CARDS.forEach(function (c, i) {
    var el = document.getElementById("c" + i);
    c.i = i;
    common(el, c, c.start, c.dur);
    tl = gsap.timeline();
    (A[c.kind] || function () {})(el, c, 0, c.dur);
    var need = NATURAL[c.kind] || 2, k = Math.min(1, Math.max(0.35, (c.dur - 1.4) / need));
    tl.timeScale(1 / k);
    var sub = tl; tl = master;
    tl.add(sub, c.start);
  });
  window.__timelines = window.__timelines || {};
  window.__timelines["root"] = tl;
})();
