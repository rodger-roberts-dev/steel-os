// "Tell us" links on the Help pages. On steel-os.org they open the report
// form there. In the Help built into Steel OS (served on this computer by
// steel-os-help-server) they open the Report a problem window instead, which
// files the same report and adds the computer details by itself. If that
// can't start, the website's form opens as before.
(function () {
  var host = location.hostname;
  if (host !== '127.0.0.1' && host !== 'localhost') return;
  document.addEventListener('click', function (ev) {
    var a = ev.target.closest && ev.target.closest('a[href="https://steel-os.org/report"]');
    if (!a) return;
    ev.preventDefault();
    fetch('/report-a-problem', { method: 'POST' })
      .then(function (r) { if (!r.ok) throw new Error(r.status); })
      .catch(function () { window.open(a.href, '_blank', 'noopener'); });
  });
})();
