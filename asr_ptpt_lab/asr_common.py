"""
KS-834: shared Azure Speech helpers for the European Portuguese (pt-PT) ASR tester.

Mirrors production (picmeinserver DddAsr AsrEngineAzure):
  - audio is pushed as 8 kHz / 16-bit / mono PCM — the hub's telephone-band rate — through a
    push stream into continuous recognition,
  - an optional phrase list is attached with weight 1.5 (AsrEngineAzure.BOOST_WEIGHT).
Anything recorded at a higher rate is resampled to 8 kHz first, so lab results reflect what the
recognizer hears in a real call rather than a studio-quality microphone.
"""
import os
import re
import threading
import time
import unicodedata
from math import gcd
from pathlib import Path

import numpy as np
import soundfile as sf
from dotenv import load_dotenv
from scipy.signal import resample_poly

import azure.cognitiveservices.speech as speechsdk

ROOT = Path(__file__).parent
LANGUAGE = "pt-PT"
HUB_RATE = 8000
BOOST_WEIGHT = 1.5  # AsrEngineAzure.BOOST_WEIGHT

# Proposed pt-PT fall boost list — the Portuguese counterpart of
# ContextDistressFallDetected.getAsrBoostPhrases(). Lives in data/boost/; boost_v2 at weight 1.5 won
# the KS-834 comparison (results/v1_w15, v1_w20, v2_w15, v2_w20). Weight 2.0 over-boosts: it made
# the recognizer insert "Nã Nã Nã" into answers that did not contain it.
PT_BOOST_FILE = ROOT / "data/boost/boost_v2.txt"
PT_BOOST_PHRASES = [l.strip() for l in open(PT_BOOST_FILE, encoding="utf-8")
                    if l.strip() and not l.startswith("#")]


def load_config():
    load_dotenv(ROOT / ".env")
    key = os.environ.get("AZURE_SPEECH_KEY")
    region = os.environ.get("AZURE_SPEECH_REGION")
    if not key or not region:
        raise SystemExit("Set AZURE_SPEECH_KEY and AZURE_SPEECH_REGION in asr_ptpt_lab/.env "
                         "(see .env.example) — use a dev key, not the production one.")
    return key, region


def speech_config(key, region, language=LANGUAGE):
    cfg = speechsdk.SpeechConfig(subscription=key, region=region)
    cfg.speech_recognition_language = language
    return cfg


def to_hub_pcm(samples, rate):
    """float/int samples at any rate (mono or stereo) -> 8 kHz int16 mono bytes."""
    x = np.asarray(samples)
    if x.ndim > 1:
        x = x.mean(axis=1)
    if x.dtype.kind == "i":
        x = x.astype(np.float32) / 32768.0
    if rate != HUB_RATE:
        g = gcd(int(rate), HUB_RATE)
        x = resample_poly(x, HUB_RATE // g, int(rate) // g)
    return (np.clip(x, -1.0, 1.0) * 32767).astype(np.int16).tobytes()


def make_recognizer(cfg, phrases=None, weight=BOOST_WEIGHT):
    fmt = speechsdk.audio.AudioStreamFormat(samples_per_second=HUB_RATE, bits_per_sample=16, channels=1)
    stream = speechsdk.audio.PushAudioInputStream(stream_format=fmt)
    audio = speechsdk.audio.AudioConfig(stream=stream)
    rec = speechsdk.SpeechRecognizer(speech_config=cfg, audio_config=audio)
    if phrases:
        plist = speechsdk.PhraseListGrammar.from_recognizer(rec)
        plist.setWeight(weight)
        for p in phrases:
            plist.addPhrase(p)
    return rec, stream


def recognize_wav(cfg, wav_path, phrases=None, realtime=False, chunk_ms=20, weight=BOOST_WEIGHT):
    """Recognize one file the way the server does. Returns dict(text, finals, partials, error, ms).

    realtime=True paces the push at real speed (as the hub does); False pushes as fast as possible,
    which Azure accepts and is much quicker for batch evaluation.
    """
    samples, rate = sf.read(str(wav_path))
    pcm = to_hub_pcm(samples, rate)
    # Trailing silence so the recognizer endpoints the last word instead of waiting for more audio.
    pcm += b"\x00\x00" * int(HUB_RATE * 0.8)
    rec, stream = make_recognizer(cfg, phrases, weight)
    finals, partials, errors = [], [], []
    done = threading.Event()

    def on_recognized(evt):
        if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech and evt.result.text:
            finals.append(evt.result.text)

    def on_canceled(evt):
        d = evt.cancellation_details
        if d.reason == speechsdk.CancellationReason.Error:
            errors.append(f"{d.error_code}: {d.error_details}")
        done.set()

    rec.recognized.connect(on_recognized)
    rec.recognizing.connect(lambda evt: partials.append(evt.result.text))
    rec.canceled.connect(on_canceled)
    rec.session_stopped.connect(lambda evt: done.set())

    start = time.perf_counter()
    rec.start_continuous_recognition_async().get()
    step = int(HUB_RATE * 2 * chunk_ms / 1000)
    for i in range(0, len(pcm), step):
        stream.write(pcm[i:i + step])
        if realtime:
            time.sleep(chunk_ms / 1000)
    stream.close()
    done.wait(timeout=30)
    rec.stop_continuous_recognition_async().get()
    return {"text": " ".join(finals).strip(), "finals": finals, "partials": partials,
            "error": "; ".join(errors), "ms": (time.perf_counter() - start) * 1000}


# --- scoring ------------------------------------------------------------------------------------

def normalise(text, keep_accents=True):
    """Lowercase, drop punctuation, collapse spaces. Accents kept by default: 'caí' vs 'cai' and
    'dói' vs 'doi' carry meaning, so stripping them would hide real recognition errors."""
    t = (text or "").lower().replace("’", "'")
    if not keep_accents:
        t = "".join(c for c in unicodedata.normalize("NFD", t) if unicodedata.category(c) != "Mn")
    t = re.sub(r"[^\w\s'-]", " ", t)
    t = t.replace("-", " ")
    return re.sub(r"\s+", " ", t).strip()


# Negated forms are checked first so "não caí" / "não me magoei" do not count as a fall.
# NAO also covers the Azorean "nã" and an unaccented "nao" from the recognizer.
NAO = r"n(?:ão|ao|ã)"
_SAFE_NEGATED = [rf"\b{NAO} ca[ií]\b", rf"\b{NAO} (?:me )?magoei\b", rf"\b{NAO} (?:me )?d[oó]i\b",
                 rf"\b{NAO} preciso de ajuda\b", rf"\b{NAO} me aleijei\b"]
_HELP = [rf"\b{NAO} estou bem\b", rf"\b{NAO} est[aá] tudo bem\b", r"\bajud[ae]\b", r"\bsocorro\b",
         r"\bca[ií]\b", r"\bd[oó]i\b", r"\bdores\b", r"\bmagoei\b", r"\baleijei\b",
         rf"\b{NAO} (?:me )?consigo\b", r"\bsangue\b", r"\bsangrar\b", r"\bpartid[oa]\b",
         r"\btonturas?\b", r"\bno ch[aã]o\b"]
_SAFE = [r"\b(?:estou|tou|tô) bem\b", r"\b(?:est[aá]|tá) tudo bem\b", r"\btudo bem\b", r"\bfoi s[oó]\b",
         rf"\b{NAO} foi nada\b", r"\bestou [oó]p?tim[oa]\b"]
_YES_WORDS = {"sim", "pois", "claro", "senhora", "senhor", "obrigado", "obrigada", "pode", "ser"}
_NO_WORDS = {"não", "nã", "nao", "nada", "obrigado", "obrigada", "senhora", "senhor", "menina",
             "quero", "é", "preciso"}


def intent_of(text):
    """Rule-based intent for the agreed answers: help / safe / yes / no / other."""
    t = normalise(text)
    neutral = t
    for rx in _SAFE_NEGATED:
        neutral = re.sub(rx, " ", neutral)
    if any(re.search(rx, neutral) for rx in _HELP):
        return "help"
    if neutral != t or any(re.search(rx, t) for rx in _SAFE):
        return "safe"
    words = t.split()
    if words and words[0] in ("sim", "pois", "claro") and set(words) <= _YES_WORDS:
        return "yes"
    if words and words[0] in ("não", "nã", "nao") and set(words) <= _NO_WORDS:
        return "no"
    return "other"
