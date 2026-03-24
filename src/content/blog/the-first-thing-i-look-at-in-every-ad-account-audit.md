---
title: "The First Thing I Look At In Every Ad Account Audit"
description: "The first thing I check in every ad account audit isn't keywords or bids — it's conversion tracking. If your tracking is wrong, every metric is a lie."
pubDate: 2026-03-23
topic: "Conversion Tracking Audits"
seo_keywords: "google ads audit, conversion tracking setup, ad account audit, google ads conversion tracking, meta pixel setup"
draft: false
---

**The first thing I look at in every ad account audit isn't what you think.**

It's not the keywords. It's not the ad copy. It's not the bid strategy or the budget or the campaign structure. I've audited hundreds of accounts over eight years and the first thing I check every single time is conversion tracking.

Because if your conversion tracking is wrong, every other metric in the account is a lie.

I took over a client's account last year where the previous agency was reporting a $45 cost per lead and a 12% conversion rate. Looked great on paper. The client was confused because the phone wasn't ringing. So I opened the tracking setup and found the problem in about 90 seconds. They were counting page views of the thank-you page as conversions, but the form was also redirecting to the thank-you page on validation errors. Every failed form submission was being counted as a lead. The real conversion rate was under 3%. The real cost per lead was over $180.

This isn't a rare edge case. This is what I find in the majority of accounts I audit. Duplicate conversion actions. Conversions counting clicks instead of actual submissions. Google Analytics goals that haven't been updated since 2019. Meta pixels firing on every page load instead of on actual events. Enhanced conversions configured but not actually sending data.

Here's another one. A client was running Meta ads for a multi-location business. Attribution looked solid in Meta's dashboard — 40 leads last month, great cost per acquisition. But when I checked Hyros against the actual CRM data, half those leads didn't exist. Meta was counting click-throughs that never converted as conversions because the attribution window was set to 7-day click and the pixel was misconfigured. The URL rules weren't matching the click parameters Meta was actually sending.

The fix took two hours. Reconfigured the URL rules, aligned the attribution windows, verified the data against actual form submissions. Suddenly the account looked completely different — and the optimization decisions changed completely because we were finally working with real numbers.

This is why I built my practice around tracking infrastructure first, campaign management second. If you optimize campaigns based on bad data, you're just making confident decisions in the wrong direction. It's worse than no data at all because it gives you false certainty.

Before you change a single bid, pause a single keyword, or rewrite a single ad, make sure you actually know what's working. The rest is noise until the foundation is right.
