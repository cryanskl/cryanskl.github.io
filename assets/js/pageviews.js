window.addEventListener('DOMContentLoaded', function () {
  try {
    // ✅ 避免重复初始化 LeanCloud
    if (!window._AV_INITED) {
      AV.init({
        appId: 'ZXG9QQe58BFo3O4clJgHOB8O-gzGzoHsz',
        appKey: 'H7Uj9y0oc0upwZxGe7J3kW6W',
        serverURLs: 'https://zxg9qqe5.lc-cn-n1-shared.com'
      });
      window._AV_INITED = true;
    }

    const Counter = AV.Object.extend('Counter');
    const path = window.location.pathname;

    const query = new AV.Query('Counter');
    query.equalTo('path', path);
    query.first().then(counter => {
      if (counter) {
        counter.increment('views');
        return counter.save();
      } else {
        const newCounter = new Counter();
        newCounter.set('path', path);
        newCounter.set('views', 1);
        const acl = new AV.ACL();
        acl.setPublicReadAccess(true);
        acl.setPublicWriteAccess(true);
        newCounter.setACL(acl);
        return newCounter.save();
      }
    }).then(result => {
      const pv = result.get('views') || 1;
      const pvSpan = document.getElementById('leancloud_pv');
      if (pvSpan) pvSpan.innerText = pv;
    });

    const sumQuery = new AV.Query('Counter');
    sumQuery.find().then(results => {
      const total = results.reduce((sum, obj) => sum + (obj.get('views') || 0), 0);
      const totalSpan = document.getElementById('leancloud_total');
      if (totalSpan) totalSpan.innerText = total;
    });

  } catch (err) {
    console.warn('[LeanCloud Pageviews Error]', err);
  }
});
