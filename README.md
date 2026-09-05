# Church Sentiment Analysis — Congregation Response Panel

> Aggregate, anonymous feedback for preachers: what happened in the room during each part of the message.

**Read this in:** English · [Português](README.pt-BR.md) · [हिन्दी](README.hi.md) · [বাংলা](README.bn.md) · [العربية](README.ar.md) · [中文](README.zh-CN.md) · [日本語](README.ja.md)

## Why
In a Pew Research survey (2016), 83% of people who had looked for a new church said the quality of the sermons mattered in their choice — the most cited factor. Yet most preachers receive only "good sermon" at the door. This project gives a preacher an objective, anonymous and aggregate view of how the congregation responded, minute by minute, linked to the transcript of the message, so the next message can be prepared better.

## What it does
- Reads a recorded service (a video file).
- Detects faces in audience shots and measures, per 30-second window, aggregate values only: number of measurable faces, % facing the stage, % smiling, expressiveness.
- Transcribes the pulpit audio and segments the service into moments (worship, prayer, announcements, sermon, call).
- Finds sustained rises and drops and writes 3 to 8 insights, each with the minute, the moment, the quoted passage and the signals used.

## What it never does (enforced by code and CI)
1. Never stores a frame, a face crop or a copy of the video.
2. Never identifies anyone: no face recognition, no embeddings, no tracking between frames, no link to membership records.
3. Never reports a window with fewer than 10 measurable faces; nothing per seat, small section or person.
4. Never says what people "felt"; wording is restricted to observed reaction.
5. Never ranks preachers or evaluates members.

## How it runs
The same Docker image runs everywhere:
- Proof of concept: Hugging Face Jobs on the cheapest GPU (T4 small, about US$0.40 per hour; roughly US$0.30–1.10 per service). See `docs/hf-jobs.md`.
- Production: a local NVIDIA server inside the church, 100% on-premises. See `docs/onprem.md`.

Quick start (local, mock engine, no GPU):
```
uv run processar_culto.py --video service.mp4 --culto 2026-09-06-19h --provider mock --out out/
```

## Status and roadmap
- Phase 0 (now): proof of concept on publicly available sermon videos that allow download; gate with six measurable criteria (`docs/poc-gate.md`).
- Phase 1: pilot with one church (4 services), after a privacy impact assessment and notice to the congregation.
- Later: live panel for the media booth and a discreet signal to the preacher.

## For churches in other countries
Legal requirements differ (GDPR, LGPD and others). The rules in "What it never does" are the minimum; check local law before processing your own recordings. Translations, validation datasets and notes on local law are welcome.

## Contributing
See `CONTRIBUTING.md`. To add a language, copy `README.md` to `README.<lang>.md` and add the link above.

## License
Apache-2.0 for this code. Third-party models keep their own licenses (see `docs/adr/0001-motor.md`).

## Origin
Started at Primeira Igreja Batista de Campo Grande, Brazil, by Fabio Pinheiro as a volunteer project, to serve preachers everywhere. "Go and make disciples of all nations" (Matthew 28:19).
