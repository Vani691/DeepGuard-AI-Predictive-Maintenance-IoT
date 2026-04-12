import requests
from datetime import datetime

# You will replace this with your actual Discord Webhook URL later
WEBHOOK_URL = "YOUR_DISCORD_WEBHOOK_URL_HERE"

def send_discord_alert(engine_id, cycle, risk_type, probability):
    """Sends a formatted embedded message to a Discord channel."""
    
    if WEBHOOK_URL == "https://discord.com/api/webhooks/1492917324951322794/ag-EDIza-_Uqq6bS0jrjdxHrikuAi-oyu9nd3jZdmG3b-qfeKQ3YaVb2PvYoq1mHxQ17":
        print("Webhook URL not set. Skipping live alert.")
        return 

    # Use Red for predictive failure, Orange for unknown anomalies
    color = 16711680 if "FAILURE" in risk_type else 16753920 

    payload = {
        "embeds": [{
            "title": "🚨 DEEP-GUARD: CRITICAL TELEMETRY ALERT",
            "description": f"**Engine ID `{engine_id}`** has crossed the critical risk threshold.",
            "color": color,
            "fields": [
                {"name": "Flight Cycle", "value": str(cycle), "inline": True},
                {"name": "Trigger Type", "value": risk_type, "inline": True},
                {"name": "AI Confidence", "value": f"{probability*100:.1f}%", "inline": True},
                {"name": "System Timestamp", "value": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S")), "inline": False}
            ],
            "footer": {"text": "AI Predictive Maintenance Engine • Automated Dispatch"}
        }]
    }

    try:
        requests.post(WEBHOOK_URL, json=payload)
        print(f"✅ Live alert dispatched for Engine {engine_id}!")
    except Exception as e:
        print(f"❌ Webhook failed: {e}")