# Companion trend reports

Six executive reports researched September 21, 2026, using the approved AI capability and adoption report’s design. All are ready for review. The AI pilot is unchanged.

| Report | Source entries | Evidence and update notes |
|---|---:|---|
| [Business succession](../../../trends/01-business-succession.html) | 11 | [Records](../business-succession/README.md) |
| [Private equity](../../../trends/02-pe-returns-and-capital.html) | 11 | [Records](../pe-returns-and-capital/README.md) |
| [Labor and knowledge](../../../trends/04-labor-and-institutional-knowledge.html) | 12 | [Records](../labor-and-institutional-knowledge/README.md) |
| [Agent-mediated distribution](../../../trends/05-agent-mediated-distribution.html) | 11 | [Records](../agent-mediated-distribution/README.md) |
| [Software and services](../../../trends/06-commoditization-of-software-and-services.html) | 12 | [Records](../commoditization-of-software-and-services/README.md) |
| [Data and private AI](../../../trends/07-business-data-and-private-ai.html) | 14 | [Records](../business-data-and-private-ai/README.md) |

Each HTML file is self-contained for offline reading, apart from external citations and linked repository records. Charts use labeled source values or explicitly hypothetical inputs. No new interviews, paid databases or proprietary research were obtained.

These are selective evidence reviews, not systematic reviews or a claim to have located every relevant release. Source registers identify methods, dates, limitations and abstract/summary-only access where applicable. Company metrics and announcements are not treated as independent causal evaluations. Multiple pages from one study are not independent corroboration. Report dates and observation dates differ.

## Maintaining the reports

The numbered content files hold the report text, cases, source metadata and chart inputs. `build_reports.py` generates the six HTML reports and evidence records. It takes the shared CSS and navigation behavior from the approved AI report without editing it.

To rebuild after editing the content, run `python3 research/data/trend-reports/build_reports.py` from the project root. Update research dates when undertaking a new evidence review. Verify calculations, source support, internal links, mobile layouts and print output after changes. Do not edit generated evidence records alone; the next rebuild would replace them.

The company concepts remain hypotheses. Discussion notes and decisions belong in the existing notes folder; these reports establish a research foundation rather than an agreed business choice.
