# Technical opportunity underwriting: methodology and maintenance

The [technical underwriting document](../../analyses/consumer-agent-uplift.html) ranks six broad technology areas by potential net EBITA return, speed to value and technical feasibility. Sector examples support the assessment; they do not define a specific product or customer.

## Scope

The six areas are customer acquisition and conversion, customer retention and service, administrative coordination, scheduling and capacity utilization, workforce and operational efficiency, and financial operations and spend control. Each includes several possible workflows, a representative bounded scope, and simpler versus more demanding variants.

Individual-business qualification, outreach scripts, partner selection and pilot design are outside this document. No operating baseline or measured EBITA improvement is available. Scores are internal underwriting judgments, not forecasts or validated investment conclusions.

## Rubric

| Dimension | Weight | Basis |
|---|---:|---|
| Potential net EBITA return | 40% | Frequency and breadth of recoverable contribution or operating cost, net of incremental fulfillment and running costs. |
| Speed to value | 30% | Time to a useful connected implementation and a financially observable result; reuse accelerates subsequent deployments. |
| Technical feasibility | 30% | Component maturity, workflow independence, typical data accessibility, integration complexity and failure handling. |

Every dimension has explicit anchors from 1 to 5 in [map.json](map.json) and in the document. Higher is better. Weighted total = sum of each weight multiplied by its score divided by five. The builder calculates totals; they are not entered independently. Differences below five points are not decisive. A one-point return change moves the total by eight points.

Scores assess the representative connected scope, not an area's easiest feature or hardest variant. Return confidence is Low because no operating baselines are available. Speed and feasibility confidence are Medium where documented components exist but an integrated implementation is unverified. Unknown evidence is recorded as an open question rather than silently assigned a neutral score.

Reusability is discussed explicitly and contributes to repeat-deployment speed. It is not a separate score that can outweigh EBITA potential. Vendor feature overlap can favor configuration or integration rather than new software. Technical feasibility does not establish defensibility or willingness to pay.

## Economic basis

Incremental contribution from fulfilled work and actual operating-cost reductions can improve EBITA. Deduct fulfillment cost, offers, software, model usage, human review and ongoing maintenance. Count credible avoided incremental hiring separately from merely freeing staff time. Faster collections are working-capital release, not automatically EBITA. Do not count the same sale, recovered invoice or labor hour in multiple areas.

Record one-time implementation and deployment costs separately; distinguish steady-state improvement, first-year earnings and cash with consistent accounting treatment. No uplift percentages, exit-multiple expansion or company-specific ROI are assumed. No EBITA calculator is included.

## Delivery estimates

First-build ranges are engineering planning assumptions for a bounded connected product with two full-time experienced engineers, part-time operating expertise, authorized documented API access or usable exports, and no foundation-model training. They are not vendor benchmarks or commitments. They begin after access is available.

Economic observation is a separate interval after deployment. It depends on fulfillment, staffing, renewal or close cycles. The speed score covers both implementation and financial observation, so an easy administrative build does not automatically receive the highest speed rating. Access delays and specialized data or domain rules can materially extend the ranges.

## Sources and applicability

- Sector universe: [PE opportunity map](../../reports/pe-opportunity-map.html) by Lisa, originally `ai-services-sector-map v05.html`. Source HTML is preserved.
- Inclusion rule: source summary rows with `data-group="con"` and `data-risk="1"`. All 15 qualifying sectors are included; 12 have `data-exp="1"`. Experience is a filter, not a technical score.
- The combined brokerage/moving sector is excluded because the source rates it Medium. Veterinary retains the source's consumer classification; clinical scope is explicitly separated from routine administration.
- Sector applicability is analytical. Direct means a clear conceptual connection to a recurring process; Selective means a narrower fit, business-model dependence or more demanding scope. Neither establishes unmet demand, easy integration or measured uplift.
- Primary platform/product documentation is listed with findings and links in `map.json`, checked September 29, 2026. It supports component capabilities and dependencies, not the return scores, engineering ranges or vendor performance claims. Document Intelligence accuracy guidance was available as a documentation excerpt.
- Existing trend reports supply broader context. The underwriting does not independently verify the PE map's market-size or sponsor claims.

## Maintained files

- [map.json](map.json): rubric, assumptions, six area assessments, sector metadata/applicability and technical source register.
- [build.py](../../../scripts/consumer-agent-map/build.py): validates basic structure, calculates scores and generates the standalone HTML.
- [template.html](../../../scripts/consumer-agent-map/template.html): layout, explanatory text and browser interactions.

From the repository root:

```sh
python3 scripts/consumer-agent-map/build.py
```

Edit the data/template and rebuild. Keep the rubric, score explanations, conclusions and source findings consistent. Verify rankings, source links, sector coverage, sorting, expandable briefs, print behavior and mobile layout after relevant changes. The generated document embeds its content and works offline; external citations require internet access.
