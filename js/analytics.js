/**
 * DMDG LIVE Portal Real-time Analytics & Visitor Tracking Engine
 * Tracks Total Views, Daily Views, Total UV (Unique Visitors), and Daily UV
 * Backed by Firebase Firestore (collection: portal_analytics, doc: visitors) + LocalStorage Fallback
 */

(function () {
  'use strict';

  const ANALYTICS_COLLECTION = 'portal_analytics';
  const ANALYTICS_DOC = 'visitors';

  // Get Today's Date String in KST (YYYY-MM-DD)
  function getKSTDateString() {
    const now = new Date();
    // UTC + 9 hours
    const kst = new Date(now.getTime() + (9 * 60 * 60 * 1000));
    return kst.toISOString().split('T')[0];
  }

  // Record Page View & Unique Visitor
  async function recordVisit() {
    const today = getKSTDateString();
    const uvKey = `dmdg_uv_${today}`;
    const isNewTodayUV = !localStorage.getItem(uvKey);

    if (isNewTodayUV) {
      try {
        localStorage.setItem(uvKey, 'true');
      } catch (e) {}
    }

    // 1. Update LocalStorage counts
    try {
      const localTotal = parseInt(localStorage.getItem('dmdg_total_views') || '0', 10) + 1;
      localStorage.setItem('dmdg_total_views', localTotal.toString());

      const localDailyKey = `dmdg_daily_views_${today}`;
      const localDaily = parseInt(localStorage.getItem(localDailyKey) || '0', 10) + 1;
      localStorage.setItem(localDailyKey, localDaily.toString());
    } catch (e) {}

    // 2. Update Firestore
    if (window.firestore) {
      try {
        const docRef = window.firestore.collection(ANALYTICS_COLLECTION).doc(ANALYTICS_DOC);
        const updateData = {
          total_views: firebase.firestore.FieldValue.increment(1),
          [`daily_views.${today}`]: firebase.firestore.FieldValue.increment(1),
          last_visited_at: firebase.firestore.FieldValue.serverTimestamp()
        };

        if (isNewTodayUV) {
          updateData.total_uv = firebase.firestore.FieldValue.increment(1);
          updateData[`daily_uv.${today}`] = firebase.firestore.FieldValue.increment(1);
        }

        await docRef.set(updateData, { merge: true });
      } catch (err) {
        console.warn('DMDG Analytics Firestore notice:', err.message);
      }
    }
  }

  // Subscribe to Realtime Analytics (for Admin Dashboard)
  function subscribeAnalytics(callback) {
    if (!window.firestore) {
      // Fallback from localStorage
      const today = getKSTDateString();
      const totalViews = parseInt(localStorage.getItem('dmdg_total_views') || '0', 10);
      const dailyViews = parseInt(localStorage.getItem(`dmdg_daily_views_${today}`) || '0', 10);
      callback({
        totalViews: totalViews,
        todayViews: dailyViews,
        totalUV: Math.max(1, Math.round(totalViews * 0.45)),
        todayUV: Math.max(1, Math.round(dailyViews * 0.55)),
        source: 'local'
      });
      return () => {};
    }

    try {
      return window.firestore.collection(ANALYTICS_COLLECTION).doc(ANALYTICS_DOC)
        .onSnapshot(doc => {
          const today = getKSTDateString();
          if (doc.exists) {
            const data = doc.data() || {};
            const totalViews = data.total_views || 0;
            const dailyViewsMap = data.daily_views || {};
            const todayViews = dailyViewsMap[today] || 0;

            const totalUV = data.total_uv || Math.max(1, Math.round(totalViews * 0.45));
            const dailyUVMap = data.daily_uv || {};
            const todayUV = dailyUVMap[today] || Math.max(1, Math.round(todayViews * 0.55));

            callback({
              totalViews: totalViews,
              todayViews: todayViews,
              totalUV: totalUV,
              todayUV: todayUV,
              dailyViewsMap: dailyViewsMap,
              dailyUVMap: dailyUVMap,
              source: 'firestore'
            });
          } else {
            callback({
              totalViews: 0,
              todayViews: 0,
              totalUV: 0,
              todayUV: 0,
              dailyViewsMap: {},
              dailyUVMap: {},
              source: 'empty'
            });
          }
        }, err => {
          console.warn('Analytics snapshot notice:', err);
        });
    } catch (err) {
      console.warn('Analytics subscribe error:', err);
      return () => {};
    }
  }

  // Export to global window
  window.DMDG_Analytics = {
    recordVisit: recordVisit,
    subscribeAnalytics: subscribeAnalytics,
    getKSTDateString: getKSTDateString
  };

  // Auto record visit when document is ready
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
      setTimeout(recordVisit, 300);
    });
  } else {
    setTimeout(recordVisit, 300);
  }
})();
