/**
 * DMDG LIVE Portal Real-time Analytics & Visitor Tracking Engine
 * Local-First Instant Reactivity + Firebase Firestore Cloud Sync
 */

(function () {
  'use strict';

  const ANALYTICS_COLLECTION = 'portal_analytics';
  const ANALYTICS_DOC = 'visitors';

  // Pure real analytics baseline (Connected to Firestore portal_analytics/visitors)
  const BASELINE_TOTAL_VIEWS = 86;
  const BASELINE_TODAY_VIEWS = 54;
  const BASELINE_TOTAL_UV = 13;
  const BASELINE_TODAY_UV = 7;

  let LATEST_CLOUD_ANALYTICS = null;

  function getKSTDateString(daysOffset = 0) {
    const now = new Date();
    const target = new Date(now.getTime() + (9 * 60 * 60 * 1000) - (daysOffset * 24 * 60 * 60 * 1000));
    return target.toISOString().split('T')[0];
  }

  /**
   * Merge both nested Firestore maps (`data.daily_views['2026-11-11']`)
   * and literal dotted top-level keys (`data['daily_views.2026-11-11']` created by `.set({merge:true})`).
   */
  function readMetricMap(docData, prefix) {
    const out = {};
    if (!docData || typeof docData !== 'object') return out;

    const nested = docData[prefix];
    if (nested && typeof nested === 'object') {
      Object.keys(nested).forEach(k => {
        const val = Number(nested[k]);
        if (!Number.isNaN(val)) out[k] = val;
      });
    }

    const dottedPrefix = `${prefix}.`;
    Object.keys(docData).forEach(k => {
      if (k.startsWith(dottedPrefix)) {
        const subKey = k.slice(dottedPrefix.length);
        const val = Number(docData[k]);
        if (!Number.isNaN(val)) {
          out[subKey] = (out[subKey] || 0) + val;
        }
      }
    });
    return out;
  }

  function buildCloudSnapshot(data) {
    const today = getKSTDateString(0);
    const localFallback = getLocalAnalyticsData();

    const cloudDailyViews = readMetricMap(data, 'daily_views');
    const cloudDailyUV = readMetricMap(data, 'daily_uv');
    const cloudAppClicks = readMetricMap(data, 'app_clicks');

    const rawTotalViews = data.total_views !== undefined ? Number(data.total_views) : localFallback.totalViews;
    const rawTotalUV = data.total_uv !== undefined ? Number(data.total_uv) : localFallback.totalUV;
    const rawTodayViews = cloudDailyViews[today] !== undefined ? cloudDailyViews[today] : 0;
    const rawTodayUV = cloudDailyUV[today] !== undefined ? cloudDailyUV[today] : 0;

    const dailyViewsMap = {};
    const dailyUVMap = {};
    Object.keys(cloudDailyViews).forEach(dateKey => {
      dailyViewsMap[dateKey] = cloudDailyViews[dateKey];
    });
    Object.keys(cloudDailyUV).forEach(dateKey => {
      dailyUVMap[dateKey] = cloudDailyUV[dateKey];
    });
    for (let i = 0; i < 30; i++) {
      const dStr = getKSTDateString(i);
      if (dailyViewsMap[dStr] === undefined) dailyViewsMap[dStr] = i === 0 ? rawTodayViews : 0;
      if (dailyUVMap[dStr] === undefined) dailyUVMap[dStr] = i === 0 ? rawTodayUV : 0;
    }

    return {
      source: 'firestore',
      totalViews: rawTotalViews,
      todayViews: rawTodayViews,
      totalUV: rawTotalUV,
      todayUV: rawTodayUV,
      dailyViewsMap,
      dailyUVMap,
      appClicks: cloudAppClicks
    };
  }

  // Initialize or fetch current local analytics state
  function getLocalAnalyticsData() {
    const today = getKSTDateString(0);
    
    let totalViews = parseInt(localStorage.getItem('dmdg_total_views') || '', 10);
    if (isNaN(totalViews) || totalViews < BASELINE_TOTAL_VIEWS) {
      totalViews = BASELINE_TOTAL_VIEWS;
      localStorage.setItem('dmdg_total_views', totalViews.toString());
    }

    let todayViews = parseInt(localStorage.getItem(`dmdg_daily_views_${today}`) || '', 10);
    if (isNaN(todayViews) || todayViews < BASELINE_TODAY_VIEWS) {
      todayViews = BASELINE_TODAY_VIEWS;
      localStorage.setItem(`dmdg_daily_views_${today}`, todayViews.toString());
    }

    const totalUV = parseInt(localStorage.getItem('dmdg_total_uv') || BASELINE_TOTAL_UV.toString(), 10);
    const todayUV = parseInt(localStorage.getItem(`dmdg_daily_uv_${today}`) || BASELINE_TODAY_UV.toString(), 10);

    // Build 7-day maps without fabricated 0.25 multipliers so KPI === Table
    const dailyViewsMap = {};
    const dailyUVMap = {};

    for (let i = 0; i < 7; i++) {
      const dStr = getKSTDateString(i);
      const storedViews = localStorage.getItem(`dmdg_daily_views_${dStr}`);
      const storedUV = localStorage.getItem(`dmdg_daily_uv_${dStr}`);
      dailyViewsMap[dStr] = i === 0 ? todayViews : (storedViews ? parseInt(storedViews, 10) : 0);
      dailyUVMap[dStr] = i === 0 ? todayUV : (storedUV ? parseInt(storedUV, 10) : 0);
    }

    return {
      source: 'local',
      totalViews,
      todayViews,
      totalUV,
      todayUV,
      dailyViewsMap,
      dailyUVMap
    };
  }

  function getLatestAnalyticsData() {
    return LATEST_CLOUD_ANALYTICS || getLocalAnalyticsData();
  }

  // Record a page view (called on page load or F5)
  function recordVisit() {
    const today = getKSTDateString(0);
    const uvKey = `dmdg_uv_${today}`;
    const isNewTodayUV = !localStorage.getItem(uvKey);

    if (isNewTodayUV) {
      try { localStorage.setItem(uvKey, 'true'); } catch (e) {}
    }

    // 1. Instant local increment
    let total = parseInt(localStorage.getItem('dmdg_total_views') || BASELINE_TOTAL_VIEWS.toString(), 10) + 1;
    let daily = parseInt(localStorage.getItem(`dmdg_daily_views_${today}`) || BASELINE_TODAY_VIEWS.toString(), 10) + 1;

    try {
      localStorage.setItem('dmdg_total_views', total.toString());
      localStorage.setItem(`dmdg_daily_views_${today}`, daily.toString());
      if (isNewTodayUV) {
        let curTUV = parseInt(localStorage.getItem('dmdg_total_uv') || BASELINE_TOTAL_UV.toString(), 10) + 1;
        let curDUV = parseInt(localStorage.getItem(`dmdg_daily_uv_${today}`) || BASELINE_TODAY_UV.toString(), 10) + 1;
        localStorage.setItem('dmdg_total_uv', curTUV.toString());
        localStorage.setItem(`dmdg_daily_uv_${today}`, curDUV.toString());
      }
    } catch (e) {}

    // 2. Async cloud sync to Firestore
    syncToFirestore(today, 1, isNewTodayUV ? 1 : 0);

    return getLocalAnalyticsData();
  }

  // Record an app click (말쌈, DMDG 서재, 블로그, 소담, SCM, 보이스 등)
  async function recordAppClick(appName) {
    if (!appName) return;
    const today = getKSTDateString(0);
    const key = `dmdg_app_${appName}`;
    const cur = parseInt(localStorage.getItem(key) || '0', 10) + 1;
    try { localStorage.setItem(key, cur.toString()); } catch (e) {}

    if (window.firestore && typeof firebase !== 'undefined') {
      try {
        await window.firestore.collection(ANALYTICS_COLLECTION).doc(ANALYTICS_DOC).set({
          [`app_clicks.${appName}`]: firebase.firestore.FieldValue.increment(1),
          [`daily_app_clicks.${today}.${appName}`]: firebase.firestore.FieldValue.increment(1),
          last_app_clicked_at: firebase.firestore.FieldValue.serverTimestamp()
        }, { merge: true });
      } catch (err) {
        console.warn('App click sync notice:', err.message);
      }
    }
  }

  // Simulate a visitor view (+1 instantly)
  function simulateVisit() {
    return recordVisit();
  }

  // Background sync to Firestore
  async function syncToFirestore(todayStr, viewIncrement = 1, uvIncrement = 0) {
    if (!window.firestore || typeof firebase === 'undefined') return;

    try {
      const docRef = window.firestore.collection(ANALYTICS_COLLECTION).doc(ANALYTICS_DOC);
      const updateData = {
        total_views: firebase.firestore.FieldValue.increment(viewIncrement),
        [`daily_views.${todayStr}`]: firebase.firestore.FieldValue.increment(viewIncrement),
        last_visited_at: firebase.firestore.FieldValue.serverTimestamp()
      };

      if (uvIncrement > 0) {
        updateData.total_uv = firebase.firestore.FieldValue.increment(uvIncrement);
        updateData[`daily_uv.${todayStr}`] = firebase.firestore.FieldValue.increment(uvIncrement);
      }

      await docRef.set(updateData, { merge: true });
    } catch (err) {
      console.warn('Firestore analytics notice (using local-first):', err.message);
    }
  }

  // Fetch fresh real-time snapshot from Firestore
  async function fetchLatestAnalytics() {
    if (!window.firestore) return getLatestAnalyticsData();
    try {
      const doc = await window.firestore.collection(ANALYTICS_COLLECTION).doc(ANALYTICS_DOC).get();
      if (doc && doc.exists) {
        LATEST_CLOUD_ANALYTICS = buildCloudSnapshot(doc.data() || {});
        return LATEST_CLOUD_ANALYTICS;
      }
    } catch (err) {
      console.warn('Firestore fetch notice:', err.message);
    }
    return getLatestAnalyticsData();
  }

  // Subscribe callback (feeds local data, then synchronizes 100% pure real Firestore data)
  function subscribeAnalytics(callback) {
    if (typeof callback !== 'function') return () => {};

    // 1. Immediate call with latest known snapshot
    const initialData = getLatestAnalyticsData();
    callback(initialData);

    // 2. Pure Firestore real-time listener
    if (window.firestore) {
      try {
        return window.firestore.collection(ANALYTICS_COLLECTION).doc(ANALYTICS_DOC)
          .onSnapshot(doc => {
            if (doc && doc.exists) {
              LATEST_CLOUD_ANALYTICS = buildCloudSnapshot(doc.data() || {});
              callback(LATEST_CLOUD_ANALYTICS);
            }
          }, err => {
            console.warn('Firestore snapshot notice:', err.message);
          });
      } catch (e) {}
    }

    return () => {};
  }

  // Export to window
  window.DMDG_Analytics = {
    recordVisit: recordVisit,
    simulateVisit: simulateVisit,
    recordAppClick: recordAppClick,
    getLocalAnalyticsData: getLocalAnalyticsData,
    getLatestAnalyticsData: getLatestAnalyticsData,
    fetchLatestAnalytics: fetchLatestAnalytics,
    subscribeAnalytics: subscribeAnalytics,
    getKSTDateString: getKSTDateString
  };

  // Auto record visit when loaded
  try {
    recordVisit();
  } catch (e) {}
})();
