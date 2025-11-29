import os
from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse
from supabase import create_client, Client

app = Flask(__name__)

ELEVENLABS_ENDPOINT = "https://api.us.elevenlabs.io/twilio/inbound_call"

# Initialize Supabase client
supabase_url = os.environ.get("SUPABASE_URL")
supabase_key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)


def is_phone_registered(phone: str) -> bool:
    """Check if a phone number exists in the users table."""
    try:
        response = supabase.table("users").select("id").eq("phone", phone).execute()
        return len(response.data) > 0
    except Exception as e:
        print(f"Database error checking phone {phone}: {e}")
        return False


@app.route("/twilio-gateway", methods=["POST"])
def twilio_gateway():
    caller = request.form.get("From")
    call_sid = request.form.get("CallSid")

    # ---- CUSTOM ACCESS LOGIC ----
    # Check if phone number is registered in database
    if not is_phone_registered(caller):
        vr = VoiceResponse()
        vr.say("Access denied. Your phone number is not registered.")
        vr.hangup()
        return Response(str(vr), mimetype="text/xml")

    # ---- FORWARD TO ELEVENLABS INBOUND ENDPOINT ----
    vr = VoiceResponse()
    vr.redirect(ELEVENLABS_ENDPOINT)
    return Response(str(vr), mimetype="text/xml")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

