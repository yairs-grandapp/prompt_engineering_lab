# KS-835 Azure first pass — listening notes (João, native pt-PT speaker, 2026-10-09)

Judged on the 16 kHz files (hub playback rate) in listen.html.

## Shortlist

| Rank | Voice | Kind | Status | TTFA median |
|---|---|---|---|---|
| 1 | pt-PT-RaquelNeural | native pt-PT neural | GA | ~440 ms |
| 2 | pt-PT-FernandaNeural | native pt-PT neural | GA | ~210 ms |
| 3 | en-US-Ava:DragonHDLatestNeural | multilingual HD, speaks pt-PT via `<lang xml:lang="pt-PT">` | GA | ~280 ms |

Overall preference: Raquel. Taking everything into account (speaking pace, tone of voice, naturalness),
it sounds best in general. Its slower pace (the longest clips) suits elderly listeners.

## AWS Polly (results/polly_first_pass) and final decision

Polly has one European Portuguese voice suitable for VEGA: Ines (female, neural); Cristiano is male and
standard-only. Ines starts fastest (~80 ms to first audio on a warm connection, region eu-south-2), but after
listening to all four side by side (results/compare_shortlist.html), **pt-PT-RaquelNeural (Azure) is the
final choice**: it sounds best overall.

## Discarded

- pt-PT-Harper:MAI-Voice-2.1-Flash (preview): acceptable (ranked 4th), but not shortlisted.
- pt-PT-Harper:MAI-Voice-2.1 (HD, preview): a slight Brazilian accent, and the slowest start (~880 ms).
- pt-BR-Thalita:DragonHDLatestNeural: a Brazilian voice speaking pt-PT; not usable.

## Notes for integration (KS-836)

- Ava is an en-US voice: production must send SSML with `<lang xml:lang="pt-PT">` around the text, or it
  speaks with English rules. Its "alert" clip is noticeably shorter (3.0 s vs ~5 s), so check it says the
  whole line.
- TTFA was measured from a PC in Portugal to Azure West Europe on a warm connection; re-measure from the server.
