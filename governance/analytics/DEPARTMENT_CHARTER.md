# Analytics Intelligence Department (AID)

**Soru:** Kullanıcı uygulamada gerçekten ne yapıyor?  
**Durum:** v2 — Sprint P pipeline (Room + Firebase remote)  
**Agent rule:** `.cursor/rules/16-analytics-intelligence.mdc`

---

## Üretir

| Dosya | Açıklama |
|-------|----------|
| `output/live_metrics.json` | Sprint P canlı metrik çerçevesi |
| `output/retention_snapshot.json` | D1/D7/D30 |
| `output/churn_signals.json` | Churn risk sinyalleri |
| `output/session_analysis.json` | Session length, daily practice rate |
| `output/feature_adoption.json` | Feature adoption |
| `output/completion_metrics.json` | Learning completion |

**Script:** `scripts/analytics/build_aid_output.py`  
**Doğrulama:** `scripts/analytics/validate_sprint_p_activation.py`  
**Döngü:** `scripts/analytics/run_aid_cycle.sh`

---

## Sprint P (P0)

**Gate:** `SPRINT_P_ACTIVATION_GATE.json`  
**Events:** `SPRINT_P_EVENT_CATALOG.json`  
**Runbook:** `SPRINT_P_ACTIVATION_RUNBOOK.md`

Başarı kriteri:

```json
{
  "live_analytics": true,
  "firebase_connected": true,
  "session_tracking": true,
  "retention_tracking": true,
  "event_pipeline": true
}
```

F002 (`phrase_*`) ve premium funnel bu katman olmadan ölçülemez.

---

## App pipeline

```
TrackAnalyticsEventUseCase
  → AnalyticsRepository
      → AnalyticsLocalDataSource (Room)
      → FirebaseAnalyticsRemoteDataSource (Firebase, when configured)
```

Session lifecycle: `AnalyticsSessionTracker` (ProcessLifecycleOwner)

---

## Not

`PIPELINE_READY`: kod hazır, Firebase credentials veya saha kanıtı bekleniyor.  
`ACTIVE`: canlı veri + Sprint P validation.
