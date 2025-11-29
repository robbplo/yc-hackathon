from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse

app = Flask(__name__)

ELEVENLABS_ENDPOINT = "https://api.us.elevenlabs.io/twilio/inbound_call"

# Example: only allow these numbers
ALLOWED_NUMBERS = {"+31636345484", "+15556667777"}


@app.route("/twilio-gateway", methods=["POST"])
def twilio_gateway():
    caller = request.form.get("From")
    call_sid = request.form.get("CallSid")

    # ---- CUSTOM ACCESS LOGIC ----
    # allowed = caller in ALLOWED_NUMBERS
    #
    # if not allowed:
    #     vr = VoiceResponse()
    #     vr.say("Access denied.")
    #     vr.hangup()
    #     return Response(str(vr), mimetype="text/xml")

    # ---- FORWARD TO ELEVENLABS INBOUND ENDPOINT ----
    vr = VoiceResponse()
    vr.redirect(ELEVENLABS_ENDPOINT)
    return Response(str(vr), mimetype="text/xml")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

