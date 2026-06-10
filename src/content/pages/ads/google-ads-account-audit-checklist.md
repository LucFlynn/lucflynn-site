---
title: "How to Audit a Google Ads Account in 30 Minutes"
slug: "google-ads-account-audit-checklist"
description: "A quick Google Ads audit checklist you can run yourself. Check targeting, keywords, conversion tracking, and budget waste in under 30 minutes."
category: "ads"
date: "2026-05-26"
hub_page: "/ads"
page_type: "spoke"
---

# How to Audit a Google Ads Account in 30 Minutes

You hired an agency three months ago, or you've been running your own ads for a while, and something feels off. The leads are thin, the spend keeps going, and the reports you're getting either look too good to be real or are full of numbers that don't mean anything. You want to know: is this account actually being managed, or is it just running on autopilot burning money?

This is the audit I run on every account I pick up. It's also what I use to train media buyers. You don't need to be technical to follow it — most of what matters is obvious once you know where to look. Budget about 30 minutes.

## The Short Answer

**Set the date range first, check conversion tracking second, then drill the hierarchy from top to bottom. The two checks that matter most if you only have ten minutes: search terms sorted by cost, and the change history.** Everything else builds on those.

## Step 1: Set Your Date Range (Don't Skip This)

Before you look at a single number, set the date range. How long has the account been running?

If it's been running more than a year, pull **365 days** — but don't stop there. You want to layer the views: **365 → 90 → 30 → 14 → 7 days.** You're looking for trends. Is CTR improving or deteriorating? Is cost per lead moving up or down over time? An account that looked fine annually might be quietly falling apart over the last 30 days. Or an account that looks rough over the full year has been cleaning up lately. The trend matters more than the snapshot.

Do this before you form any opinion. It's too easy to get a false read if you're just eyeballing the last 7 days.

## Step 2: Check Conversion Tracking First

Nothing else matters if the conversion data is wrong. I pull this before anything else because a broken conversion setup will corrupt every conclusion you draw downstream.

Go to **Tools → Conversions** and look at what's being tracked as a primary conversion action. Ask yourself:

- Does this conversion action make sense? (A phone call, a form fill, a purchase — something a real customer does.)
- Is it tagged as "Primary" and actively recording? Or is there a jumble of secondary actions, micro-conversions, and page views all mixed in and counted together?
- Could this be inflating the conversion count artificially?

The verification step is harder: you need a single source of truth outside of Google. A CRM, a spreadsheet of leads, a call log — something. Compare Google's conversion count to what you actually received. If Google says **100 conversions** and you have **10 leads in your CRM**, that's a serious problem, not a rounding error. If Google says 100 and you can count 75–130 from various sources, that's in the realm of normal — attribution is imperfect and there are legitimate reasons for some gap. Off by a factor of ten is not a measurement error; it's a broken setup.

If the tracking looks wrong, flag it immediately and note it on everything downstream. A 2% conversion rate on a broken setup might actually be 0.2%, which changes every decision you'd make. See the [conversion tracking guides](/tracking) if you need to go deep on this.

## Step 3: Get the Account-Level Snapshot

Now pull the overview — CTR, conversion rate, total cost, number of conversions — for the whole account over your date range. This becomes your benchmark. You're not judging it yet; you're getting a feel for what the baseline looks like so you can spot anomalies as you drill down.

What you're looking for at the account level:

- **CTR below 5%**: bad. Local service businesses should be pushing 9–10%+. Below 5% usually means ads are poorly matched to search terms, or match types are too loose.
- **Conversion rate below 5%**: a problem. Good accounts run 7–8%+. If the landing page is generic or mismatched to the ad, this is where it shows.
- **Spend not matching budget**: if the account's daily budget is $100 and it only spent $600 in the last 10 days instead of $1,000, it's not configured to spend. That's often a sign the structure is bad or quality scores are too low to compete in the auction.

For a full breakdown of what these numbers mean — and what ranges to actually aim for — see [how to tell if your Google Ads are working](/ads/how-to-tell-google-ads-working).

## Step 4: Drill the Campaign → Ad Group → Keyword Hierarchy

This is the structured part. Go level by level, running the same metrics at each: **CTR, conversion rate, cost, conversions, and CPC.** Apply the same date-range layering (90/30/14/7) at every level.

**Campaigns:** Which campaigns are actually producing conversions? Which are spending heavily with nothing to show? Sort by cost, then by conversions, and look for the obvious: campaigns that cost a lot and convert nothing get scrutinized first. While you're here, check the campaign settings:

- **Search Partners**: Google's partner network. Can work, but it's often lower quality than core Google Search. Worth noting if it's on.
- **Display Network**: this should almost always be **off** for a lead-gen campaign. If it's on inside a Search campaign, your search budget is silently bleeding into display inventory. This is one of Google's default-on settings that hurts a lot of accounts.
- **Performance Max**: does the account have PMax running? For e-commerce it can work well. For lead gen, I'm skeptical — PMax is a black box, and the search terms visibility is limited. If PMax is running alongside Search campaigns, check whether it's cannibalizing the same traffic.
- **Location targeting**: is a local HVAC company targeting the whole country? Does it say "People who show interest in this location" instead of "People in this location"? That second setting pulls in people researching your area from anywhere — often not what you want.
- **Bid strategy**: **tCPA (target cost per acquisition)** is the ideal for a mature account with enough conversion data. Max Conversions without a target is fine early on. Manual CPC can be too restrictive — it caps bids in a way that chokes the auction and limits spend even when there's good inventory. If someone's on Manual CPC "for control" but the account is consistently underspending, that's probably why.

**Ad Groups:** Look for ad groups with high spend and low (or zero) conversions. Check whether the ad copy in each group actually matches the keywords in that group. Mismatched themes — a "roof repair" keyword in an ad group titled "gutters" — tank [Quality Score](/ads/google-ads-quality-score-explained) and raise your CPCs.

**Keywords:** Sort by cost. Flag any keywords with high spend and zero conversions over a meaningful period — say, **$200+ spent, 0 conversions** over 30+ days. Also check match types. Broad match in the wrong hands is expensive; it'll show your ads for things you'd never have approved if someone asked you.

## Step 5: Search Terms — Read Them Like a Human

This is one of the two most important checks in the whole audit. Go to **Keywords → Search Terms**, sort by cost, and just read what comes up.

You don't need to know anything about Google Ads to know if a roofing company should be showing for "pizza restaurant." It's obvious. Apply common sense to every term on that list. Ask: would I pay for a click from someone who searched this?

What you're looking for:

- Clearly irrelevant terms (wrong industry, wrong intent, geography you don't serve)
- Competitor brand names you didn't intend to bid on
- Informational queries ("how to fix my own roof") when you're selling services
- Overly broad terms with no commercial intent

Do this over **7–30 days**, sorted by cost. The expensive irrelevant terms are the ones actively hurting you. The free ones are noise. This is also where you'll find terms worth adding as negatives — and if nobody's been adding negatives, that tells you something about how the account's been managed.

For a more complete list of what this looks like when it goes wrong, [signs your Google Ads are wasting money](/ads/signs-google-ads-wasting-money) walks through the patterns.

## Step 6: Check the Change History

This is the second of the two checks that matter most, and it's the one nobody who manages their own ads knows about.

Go to **Tools → Change History**. You'll see a log of every change ever made to the account — negative keywords added, bids adjusted, campaigns paused, ads created.

Look at the volume and recency of activity. Ask:

- **Is there any activity at all?** An account that's been running for 90 days with no entries in the change history was not being managed. It was running on autopilot.
- **What kind of activity was it?** Are there negatives being added, ads being tested, bids being refined? Or is it just a Google auto-apply recommendation touching things once a month?

**Auto-apply recommendations** deserve a specific look. Google's auto-apply feature can silently make changes to the account — adding broad match keywords, adjusting bids, expanding targeting — sometimes undoing work that a manager deliberately set up. If this is enabled and you've ever wondered why a setting you changed keeps reverting, that's likely why.

The caveat: **low activity isn't automatically bad.** At month 6 or 8 on a well-dialed account, there genuinely might not be much to do. That's fine. The red flag is the combination: **unhappy with results + 90+ days of runtime + empty change history.** That's not an account that matured past the need for management. That's an account that was never managed.

## Step 7: Act on What You Found

You've run the audit. Now connect the findings to actions.

- **Low CTR** → the problem is ad copy or keyword-to-ad alignment. The search terms aren't matching the ads well enough for people to click. Tighten the ad groups, rewrite the ads to echo the search terms more directly.
- **Low conversion rate** → the traffic is showing up, but the landing page isn't converting it. Check whether the page is specific to what the ad promised. If an ad about "emergency roof repair" lands on a generic "about us" page, you're losing those clicks. This is also where destination URLs matter — sometimes ads are sending people to the contact page instead of a relevant service page, and the business owner has no idea because they never clicked their own ad.
- **High CPC / high CPL with low conversion volume** → go back to the search terms. Wasted spend on irrelevant terms inflates both. Clean the terms, add negatives, tighten match types.
- **Conversion tracking looks off** → fix this before optimizing anything. Garbage in, garbage out.

## When to Get Help

If you've run through this and found: no activity in the change history, search terms full of irrelevant queries, conversion tracking numbers that don't match reality, and campaign settings still on their defaults — you've found a neglected account, not an optimized one.

That's actually useful information. It means there's room to improve things that aren't currently being worked on, and the wins from basic cleanup tend to be fast.

If you're not sure what you're looking at, or you found something concerning and want a second set of eyes, that's what the audit offer below is for. I'll tell you what's actually wrong and what I'd do about it — no obligation to hire anyone.

---

**Tired of guessing whether your ads are working?**

We manage Google and Meta ad accounts for businesses spending $500-$10,000/month. $800 setup, $200/month ongoing. You keep your account — we just make it work.

[→ Get a free account audit](/contact)

---
