const publicEnv = window.__HANS_NIEMANN_PUBLIC_ENV__ || {};

function isLocalHost() {
  return ["127.0.0.1", "localhost"].includes(window.location.hostname);
}

function appendScript(src) {
  const script = document.createElement("script");
  script.src = src;
  script.async = true;
  document.head.appendChild(script);
}

function enableGoogleAnalytics(measurementId) {
  if (!measurementId) {
    document.documentElement.dataset.gaEnabled = "false";
    return;
  }

  window.dataLayer = window.dataLayer || [];
  window.gtag = function gtag() {
    window.dataLayer.push(arguments);
  };
  window.gtag("js", new Date());
  window.gtag("config", measurementId, {
    anonymize_ip: true,
    transport_type: "beacon"
  });

  document.documentElement.dataset.gaEnabled = "true";
  document.documentElement.dataset.gaMeasurementId = measurementId;

  if (!isLocalHost()) {
    appendScript(
      `https://www.googletagmanager.com/gtag/js?id=${encodeURIComponent(measurementId)}`
    );
  }
}

function enableClarity(projectId) {
  if (!projectId) {
    document.documentElement.dataset.clarityEnabled = "false";
    return;
  }

  window.clarity =
    window.clarity ||
    function clarity() {
      (window.clarity.q = window.clarity.q || []).push(arguments);
    };

  document.documentElement.dataset.clarityEnabled = "true";
  document.documentElement.dataset.clarityProjectId = projectId;

  if (!isLocalHost()) {
    ((c, l, a, r, i, t, y) => {
      c[a] =
        c[a] ||
        function () {
          (c[a].q = c[a].q || []).push(arguments);
        };
      t = l.createElement(r);
      t.async = 1;
      t.src = `https://www.clarity.ms/tag/${i}`;
      y = l.getElementsByTagName(r)[0];
      y.parentNode.insertBefore(t, y);
    })(window, document, "clarity", "script", projectId);
  }
}

document.querySelectorAll(".hero-visual img[data-fallback]").forEach((image) => {
  image.addEventListener(
    "error",
    () => {
      if (image.dataset.fallback && image.src !== image.dataset.fallback) {
        image.src = image.dataset.fallback;
      }
    },
    { once: true }
  );
});

enableGoogleAnalytics(publicEnv.googleAnalyticsId || "");
enableClarity(publicEnv.clarityProjectId || "");
