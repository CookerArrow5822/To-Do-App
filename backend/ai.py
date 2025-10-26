import os
from datetime import datetime, timedelta
from typing import List, Dict, Any
from openai import OpenAI


client = None
api_key = os.getenv("OPENAI_API_KEY")
if api_key:
    client = OpenAI(api_key=api_key)


SYSTEM_PROMPT = (
    "You are a helpful planner. Given tasks with optional due windows and durations, "
    "suggest a minimal schedule for the next 7 days as ISO datetimes. "
    "Return JSON with a 'plan' array of {id, title, start, end}. Keep it simple."
)


def suggest_schedule(tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
"""Call OpenAI to propose a schedule. If no API key, return a naive fallback."""
if not client:
# Fallback: place incomplete tasks sequentially from now, 30m each.
now = datetime.utcnow().replace(microsecond=0)
cursor = now
plan = []
for t in tasks:
if t.get("is_done"):
continue
dur = int(t.get("duration_min") or 30)
start = cursor
end = start + timedelta(minutes=dur)
plan.append({
"id": t["id"],
"title": t["title"],
"start": start.isoformat() + "Z",
"end": end.isoformat() + "Z",
})
cursor = end
return {"plan": plan, "source": "fallback"}


messages = [
{"role": "system", "content": SYSTEM_PROMPT},
{"role": "user", "content": str(tasks)},
]


resp = client.chat.completions.create(
model="gpt-4o-mini",
messages=messages,
response_format={"type": "json_object"},
temperature=0.2,
)
try:
return resp.choices[0].message.model_dump().get("content") # type: ignore
except Exception:
# last‑resort: same as naive fallback
return suggest_schedule.__wrapped__(tasks) # type: ignore