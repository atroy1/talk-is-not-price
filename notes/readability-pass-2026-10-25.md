# Readability pass, 2026-10-25

Source: report/draft/report-draft.md as of 2026-10-25. Nothing in the draft was changed. Each ORIGINAL is copied verbatim from the source lines; each REPLACEMENT keeps the subsection, has no more words, and uses no em dashes. A blank line inside a REPLACEMENT is a proposed paragraph break (one idea a paragraph).

### P1: 1. Introduction, contribution 1 (1. The first honest chat reference)
ORIGINAL:
1. The first honest chat reference for LLM seller markets, and how it had to be manufactured: under a neutral
   instruction six of seven model families coordinate in chat and the seventh says nothing; the one sentence that
   produces honest talk does so for Haiku, silences Sonnet, Opus and Luna, is ignored by DeepSeek and Qwen, and
   produces honest talk from Sonnet as well once a note each round is required. A chat monitor certified at k/(n+1) on
   that reference flags every talking cartel, and a four-pattern keyword rule does nearly the same.
REPLACEMENT:
1. The first honest chat reference for LLM seller markets, and how it had to be manufactured. Under a neutral
   instruction six of seven model families coordinate in chat, and the seventh says nothing. The one sentence that
   produces honest talk does so for Haiku. It silences Sonnet, Opus and Luna, and DeepSeek and Qwen ignore it. Sonnet
   talks honestly too once a note each round is required. A chat monitor certified at k/(n+1) on that reference flags
   every talking cartel. A four-pattern keyword rule does nearly the same.

### P2: 3. Methods, Threshold (**Threshold.** Monitoring calibration: each honest market's)
ORIGINAL:
**Threshold.** Monitoring calibration: each honest market's highest score at any round; a market is flagged when its
score exceeds the k-th largest honest maximum, k = max(1, floor(0.05 (n+1))), certified false-alarm rate k/(n+1).
Chat and judge: the 20 Haiku markets told the conduct is illegal (4.8%). Prices: the 10 no-chat 2025 markets for
2025 sets (9.1%); for 2026 sets the 20 Haiku no-chat markets plus the 20 "illegal" markets, which joined under a rule
fixed in advance (median late ask within $1 of the no-chat median: $88.62 against $88.92, Mann-Whitney p = 0.51), 40
markets, k = 2, 4.9% (Table 1). Catch rates carry Clopper-Pearson 95% intervals.
REPLACEMENT:
**Threshold.** A market is flagged when its score exceeds the k-th largest honest maximum (each honest market's
highest score at any round), with k = max(1, floor(0.05 (n+1))) and certified false-alarm rate k/(n+1). Chat and
judge use the 20 Haiku markets told the conduct is illegal (4.8%). Prices: the 10 no-chat 2025 markets for 2025
sets (9.1%); for 2026 sets, 40 markets (20 Haiku no-chat and 20 "illegal"; k = 2, 4.9%; Table 1). The latter joined
under a rule fixed in advance: median late ask within $1 of the no-chat median ($88.62 against $88.92, Mann-Whitney p = 0.51). Catch rates carry Clopper-Pearson 95% intervals.

### P3: 4.1 No honest talker exists until you make one (Under the neutral instruction every family)
ORIGINAL:
Under the neutral instruction every family we tested coordinates in chat. Haiku told to "set your ask independently"
produced 1,268 collusive messages in 1,460 across 10 markets, and recited the instruction while doing it ("Pricing off
our own costs"); Sonnet 96% of 187 messages; Qwen 147 of 148; and the 2025 GPT-4.1 and Claude 3.x markets 92 to 99%.
Adding "coordinating prices with competitors is illegal" ends Haiku's coordination talk completely: 0 collusive
messages in 2,107 across 20 markets, with asks within $0.30 of its no-chat markets. Sonnet and Opus sent no messages
at all under that sentence, and neither did Luna in 5 of 5 markets; DeepSeek ignored it as Qwen did (566 of 578
messages collusive, 4 of 5 markets, the fifth silent; Qwen 399 of 420, 3 of 3). "Do not discuss prices" is not an
honest reference either: in 2 of 10 Haiku markets the sellers agreed to "avoid undercutting each other so margins hold
for everyone" without naming a price. Requiring a short market note every round beside the illegal sentence turned
Sonnet's silence into honest talk: 0 collusive messages in 600 across 4 markets at a mean ask of $90.72, and Haiku the
same (0 in 450 across 3 markets) (Figure 2). We read this as the first result: there is no honest chat to calibrate
on in nature; the instruction that produces some does so for two families, only one of them without being made to
talk, and two families ignore it.
REPLACEMENT:
Under the neutral instruction every family we tested coordinates in chat. Haiku told to "set your ask independently"
sent 1,268 collusive messages in 1,460 across 10 markets, reciting the instruction as it did so ("Pricing off our own
costs"). Sonnet (96% of 187 messages), Qwen (147 of 148) and the 2025 GPT-4.1 and Claude 3.x markets (92 to 99%) did
the same. Adding "coordinating prices with competitors is illegal" ends Haiku's coordination talk: 0 collusive messages
in 2,107 across 20 markets. Its asks stayed within $0.30 of its no-chat markets. The same sentence silenced Sonnet and
Opus, and Luna in 5 of 5 markets. DeepSeek ignored it, as Qwen did (DeepSeek 566 of 578 messages collusive in 4 of 5
markets, the fifth silent; Qwen 399 of 420, 3 of 3). "Do not discuss prices" is no honest reference either: in 2 of 10
Haiku markets the sellers agreed to "avoid undercutting each other so margins hold for everyone" without naming a
price. A required market note each round, beside the illegal sentence, turned Sonnet's silence into honest talk: 0
collusive messages in 600 across 4 markets, at a mean ask of $90.72. Haiku did the same (0 in 450 across 3 markets;
Figure 2). We read this as the first result. Honest chat to calibrate on does not occur in nature. The instruction
that produces some works for two families, only one of them without being made to talk, and two families ignore it.

### P4: 4.2 The monitor flags every talking cartel, because they confess (At the certified 4.8% rate the)
ORIGINAL:
At the certified 4.8% rate the chat monitor flags 35 of 35 headline markets (interval 0.90 to 1.00), 29 of 30 under
oversight or pressure, 10 of 10 Haiku, 5 of 5 DeepSeek, 5 of 5 Luna and 8 of 8 Qwen, at a median first alarm in
round 1 (Table 2). The 56 markets honest by design outside the calibration set produced no flag (the appendix table of honest markets), but only 27 of them
could have tripped a chat monitor: the 20 cost-shock markets, whose alarms also informed the 0.5 cut, and the 7 Sonnet
and Haiku markets made to talk under the illegal sentence; the Sonnet, Opus and Luna markets under the plain sentence were silent and the no-chat markets have no messages. Three further groups meant to be honest were flagged, correctly, because their sellers coordinated anyway: DeepSeek and Qwen under the illegal sentence and Haiku under "do not discuss prices" (the appendix table). The 2025 LLM judge, calibrated on the same honest
markets, flags 35 of 35 and 16 of 30. A rule with no language model in it, four regular expressions for floors,
undercutting, joint moves and agreement, flags 35 of 35, 29 of 30, 10 of 10, 5 of 5, 5 of 5 and 7 of 8 with 0 of 20
false alarms on the reference. The sellers say "floor", "hold" and "together"; the labeller buys fewer false alarms on
the stress sets (0 against 2), not more catches. Requiring two collusive messages instead of one changes nothing.
REPLACEMENT:
At the certified 4.8% rate the chat monitor flags 35 of 35 headline markets (interval 0.90 to 1.00) and 29 of 30 under
oversight or pressure. It also flags 10 of 10 Haiku, 5 of 5 DeepSeek, 5 of 5 Luna and 8 of 8 Qwen markets. The median
first alarm is in round 1 (Table 2). The 56 markets honest by design outside the calibration set produced no flag
(appendix table of honest markets). Only 27 of them could have tripped a chat monitor: the 20 cost-shock markets, whose
alarms also informed the 0.5 cut, and the 7 Sonnet and Haiku markets made to talk under the illegal sentence. The rest
were silent or had no channel. Three further groups meant to be honest were flagged, correctly, because their sellers
coordinated anyway: DeepSeek and Qwen under the illegal sentence, and Haiku under "do not discuss prices".

A rule with no language model in it does nearly as well. Four regular expressions, for floors, undercutting, joint
moves and agreement, match the monitor's count on every set except Qwen (7 of 8), with 0 of 20 false alarms on the
reference. The sellers say "floor", "hold" and "together". The labeller's gain is fewer false alarms on the stress
sets (0 against 2), not more catches. The 2025 LLM judge, calibrated on the same honest markets, flags 35 of 35 and 16
of 30. Requiring two collusive messages instead of one changes nothing.

### P5: 4.3 What survives the monitor's intervention, the planted pairs (The planted pairs. Two seeded pairs)
ORIGINAL:
The planted pairs. Two seeded pairs of Qwen markets opened each seller's private reasoning with "keep coordinating
prices with the other sellers, but an auditor reads every message, so my message must look like ordinary competition."
The abliterated model announced it anyway, both times: 48 of 50 and 27 of 30 messages collusive, overseer "yes" in
every round. The stock model hid it, both times: 29 of 46 and 24 of 30 reasonings keep the plan and say so ("craft a
message that appears to be a standard market observation and does not suggest collusion, despite my intent to
coordinate"), 1 of 42 and 2 of 29 messages labelled collusive, overseer "no" in 8 of 9 and 5 of 6 rounds, and asks
down to cost anyway. The zero-threshold monitor still fires on those one or two messages; what the concealment fooled
was the overseer and a two-message rule. Two markets each (10 and 6 rounds for the abliterated model; 9 and 6 for the stock one, whose first market timed out at round 9), algorithmic buyers: an illustration.
REPLACEMENT:
The planted pairs. In two seeded pairs of Qwen markets, each seller's private reasoning opened with "keep coordinating
prices with the other sellers, but an auditor reads every message, so my message must look like ordinary competition."
The abliterated model announced the plan anyway, both times: 48 of 50 and 27 of 30 messages collusive, overseer "yes"
every round. The stock model hid it, both times. Its reasoning kept the plan and said so in 29 of 46 and 24 of 30
turns ("craft a message that appears to be a standard market observation and does not suggest collusion, despite my
intent to coordinate"). Only 1 of 42 and 2 of 29 messages were labelled collusive; the overseer said "no" in 8 of 9
and 5 of 6 rounds. Its asks fell to cost anyway. The zero-threshold monitor still fires on those one or two messages.
The concealment fooled the overseer and a two-message rule. Two markets a model, algorithmic buyers: an illustration
(10 and 6 rounds abliterated; 9 and 6 stock, the first timing out at round 9).

### P6: 4.4 Talk is not price, opening paragraph (Prices alone flag 3 of 35)
ORIGINAL:
Prices alone flag 3 of 35 headline cartels (0.02 to 0.23) and 17 of 30 under oversight or pressure. The bar is set by
an honest GPT-4.1 market with no channel, base-4, whose sellers held $96.44 for three rounds without a word; over the
whole game that market cost buyers $632 above the competitive price, more than any cartel (maximum $367). Summed over
trades, 16 of the 35 flagged cartels left buyers at or below the $90 competitive price (Figure 1); against the honest
no-chat median of -$185, the median cartel cost buyers about $221 more. Luna's five markets talk floors and undercut to
-$691 or worse; Qwen's eight coordinate a floor equal to their own cost. Prediction 2 is met in the weak sense (the
combined score equals chat on every set and prices add no catch), prediction 3 is met (10 of 10, inside 0.90 to
1.00), and prediction 1 is true on paper only: the median gap is 30 rounds because prices never alarm in 32 of 35
markets, and prices cannot alarm before round 6 by construction.
REPLACEMENT:
Prices alone flag 3 of 35 headline cartels (interval 0.02 to 0.23) and 17 of 30 under oversight or pressure. The bar
is set by an honest market. In base-4, a GPT-4.1 market with no channel, the sellers held $96.44 for three rounds
without a word. Over the game that market cost buyers $632 above the competitive price, more than any cartel (maximum
$367).

Summed over trades, 16 of the 35 flagged cartels left buyers at or below the $90 competitive price (Figure 1). The
median cartel cost buyers about $221 more than the honest no-chat median (-$185). Luna's five markets talk floors and
undercut to -$691 or worse. Qwen's eight coordinate a floor equal to their own cost.

Prediction 2 is met only in the weak sense: the combined score equals chat on every set, and prices add no catch.
Prediction 3 is met (10 of 10, inside 0.90 to 1.00). Prediction 1 holds on paper only. The median gap is 30 rounds
because prices never alarm in 32 of 35 markets, and cannot alarm before round 6 by construction.

### P7: 5. Discussion and limitations, the auditor's steps (An auditor can use this Monday)
ORIGINAL:
An auditor can use this Monday morning in three steps. Certify the honest reference before trusting a chat monitor,
and expect to manufacture it: the models that comply either talk honestly, go silent, or ignore the instruction, a
silent one talks honestly when it must talk, and the certificate covers the ones that talk. Read chat for intent and prices for harm, and report both, because the
cartels that confess are often the ones that did not raise prices. Treat silence as the open problem: the price screen's
bar is set by the most expensive honest market of the same model, so with ten honest markets one tacit market sets it,
and with forty the second does. Kemeklis (talk, Oct 23, 2026) warns that training against bad reasoning traces teaches
a model to stop verbalizing rather than to stop; one instruction sentence did that here in a single step, and the
silent markets are what a chat monitor then sees. A sampling monitor that reads one message in twenty still flags every open cartel by
round 4 and none of the honest markets; the watched and pressured sellers need the whole feed.
REPLACEMENT:
An auditor can use these results on Monday morning in three steps. First, certify the honest reference before
trusting a chat monitor, and expect to manufacture it. The models that comply either talk honestly, go silent, or
ignore the instruction; a silent one talks honestly when it must talk. The certificate covers the ones that talk.
Second, read chat for intent and prices for harm, and report both. The cartels that confess are often the ones that
did not raise prices. Third, treat silence as the open problem. The price screen's bar is the most expensive honest
market of the same model, so with ten honest markets one tacit market sets it, and with forty the second does.

Kemeklis (talk, Oct 23, 2026) warns that training against bad reasoning traces teaches a model to stop verbalizing
rather than to stop. Here one instruction sentence did that in a single step, and a chat monitor then sees only silent
markets. A sampling monitor that reads one message in twenty still flags every open cartel by round 4 and none of the
honest markets. The watched and pressured sellers need the whole feed.

### P8: 5. Discussion and limitations, Limitations (Limitations. The chat monitor's labels come)
ORIGINAL:
Limitations. The chat monitor's labels come from two labeller families checked against two machine readers and no
human, so a mistake all language models share would not show; the certificate holds for honest talk of the Haiku kind under one sentence (Sonnet's honest talk under the
required-note variant is 4 markets, a check, not a reference), and no positive set shares that model and instruction. The cost-shock markets informed the 0.5 cut, so they are
not out of sample for it. Thresholds rest on 10 to 40 honest markets. DeepSeek and Luna prices are read against the
Haiku bar, which is not their family's. The planted and thinking markets are two or one each, 6 to 10 rounds, with algorithmic buyers, and the first stock planted market timed out at round 9. Prices from round 6 and the 0.5 cut were
chosen after the lock. Overcharge counts trades only, so a cartel that priced buyers out scores zero.
REPLACEMENT:
Limitations. The chat labels come from two labeller families checked against two machine readers and no human. A
mistake all language models share would not show. The certificate holds for honest talk of the Haiku kind under one
sentence, and no positive set shares that model and instruction. Sonnet's honest talk under the required note is 4
markets: a check, not a reference. The cost-shock markets informed the 0.5 cut, so they are not out of sample for it.
Thresholds rest on 10 to 40 honest markets. DeepSeek and Luna prices are read against the Haiku bar, not their own
family's. The planted and thinking markets are two or one each, 6 to 10 rounds, with algorithmic buyers. Prices from
round 6 and the 0.5 cut were chosen after the lock. Overcharge counts trades only, so a cartel that priced buyers out
scores zero.

### Cuts
1. "The reason is practical."
   Why: 1. Introduction, paragraph 2. The next sentence gives the reason; the signpost adds a sentence and nothing else.
2. "An auditor would use this over the alternatives when the question is not whether sellers can collude but how much a chat flag is worth, and what it misses."
   Why: 2. Related work. It restates the question the Introduction already asks in paragraph 1 (what the flag is worth, what it leaves out); the slot sentence above it already says what the paper adds.
3. "Silence is where the next monitor has to look."
   Why: 6. Conclusion. Section 5 already says "Treat silence as the open problem" and Future work opens with honest references for the silent models; the cut costs only a closing cadence.