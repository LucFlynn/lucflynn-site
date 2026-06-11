---
title: "Google Ads Conversion Tracking Setup Guide"
slug: "google-ads-conversion-tracking-setup"
description: "How to set up Google Ads conversion tracking correctly. Phone calls, form submissions, and the mistakes that break your data."
category: "ads"
date: "2026-05-26"
hub_page: "/ads"
page_type: "spoke"
---

# Google Ads Conversion Tracking: The Setup Nobody Gets Right

You're either in one of two situations. The first: you're not sure if your tracking is set up correctly, and every time you look at the conversion numbers you get this low-grade nausea because you can't tell if they're real. The second: you know it's broken — something clearly isn't firing, the numbers make no sense — and you can't figure out how to fix it. Either way, you've been making ad decisions based on data you don't fully trust, which means the algorithm has been making bid decisions based on data it doesn't fully trust either. That's the actual damage.

Broken tracking isn't a minor inconvenience. It's the most common reason ads fail to perform — I'd put it at the top of [the list of reasons Google Ads don't convert](/ads/google-ads-not-converting-fixes). If your tracking is wrong, everything downstream is wrong: your bidding, your budget allocation, your campaign decisions. The algorithm is literally optimizing for the wrong thing.

The fix isn't complicated, but it does require getting a few specific things right. Here's the setup.

## The Short Answer

**Track form fills and phone calls.** Set those as your conversions in Google Ads. Don't track anything else as a conversion. Install everything through Google Tag Manager. If you have a CRM and a sales team and people actually show up and buy things in person — upload those as offline conversions too, and take that seriously.

That's the whole philosophy in four sentences. The rest of this is the "why" and the specific mistakes I see constantly.

## What to Track (and What Absolutely Not to Track)

### Track These

**Form submissions.** When someone fills out your contact form, quote request form, or intake form — that's a conversion. The moment they complete the form and land on a confirmation state is the moment a conversion fires.

**Phone calls.** Most businesses don't track calls, and it's a real mistake. Calls are often your highest-quality leads — someone willing to pick up the phone is further along than someone who clicked a link. They also give you instant feedback. You answer, you talk to a real person, you immediately know whether the lead quality is there. Track them. Google Ads has a call conversion type specifically for this, and it works well.

**Offline conversions** — if you have them. If you run a business where someone fills out a form, your sales team follows up, they show up in person, and then they buy — you need to close that loop. Upload those closed deals back into Google Ads as offline conversions. It's not as scary as it sounds (your CRM can usually automate it), and it gives the algorithm the most accurate possible signal: not just "this person submitted a form" but "this person actually became a customer." That signal is genuinely powerful. Do it if you have the setup for it.

### Don't Track These as Conversions

**Page views.** It doesn't matter. Someone landing on your homepage is not a conversion. Someone landing on your about page is not a conversion. GA4 can record these events all it wants — that's fine, analytics is analytics. But if you mark them as Google Ads conversions, you've told the algorithm that getting someone to load a page is the goal. The algorithm will then optimize for page loads. You will get lots of page loads. You will not get leads.

**Link clicks.** Same problem. A click is not a completed action. Don't mark it as one.

I've seen accounts where someone set their Google Ads homepage visit as a conversion — literally "user loaded the home page." Their conversion rate looked incredible. Their cost per conversion was $4. Their leads were zero. "No, a homepage view is not a conversion. No, it's not." A conversion is: they filled out the multi-step form, they completed the application, they booked the call. That kind of thing. The bar is a completed meaningful action.

## The Right Way to Install All of This: Google Tag Manager

Don't install your GA4 tag directly on the site. Don't install your Google Ads conversion tag directly on the site. Don't install your Meta pixel directly on the site. Install **Google Tag Manager** on the site — one snippet of code — and then run GA4, the Google Ads pixel, and the Meta pixel all from inside GTM.

Why? Because when you need to change something — add a new conversion, update a tag, fix a firing condition — you do it inside GTM without touching the site code. No developer needed for most things. No risk of breaking something every time you need to adjust tracking. If you're ever running multiple ad platforms (and you should eventually be running both Google and Meta), having them all inside one container is dramatically easier to manage and audit.

The actual setup steps — which trigger to use for form submissions, how to set up call tracking, how to configure the Google Ads conversion tag inside GTM — are covered in detail in [the tracking setup library](/tracking). This article is the philosophy layer: *what* to track and *why*. Go there for the *how*.

## The Disasters I See Constantly

### The Thank-You Page That Isn't Gated

This is the most common one. The setup: you create a thank-you page (`/thank-you`), you tell Google Ads to fire a conversion when someone lands on that URL, and you move on. Looks fine. Isn't fine.

The problem is that thank-you page is often reachable directly. Someone types in the URL, or Google crawls it, or you accidentally share the link, or a past visitor bookmarks it — and every time that page loads, a conversion fires. Your conversion numbers inflate. The algorithm thinks it's doing great work when people are just loading a URL. I've seen accounts where a significant chunk of "conversions" were page loads with no preceding form submission.

The right fix is to gate the confirmation behind the actual form submission — either through a proper form-redirects-on-submit setup, or by tracking the form submission event itself rather than the destination URL. The [tracking setup guides](/tracking) cover this per form type.

### Tracking Junk Events as Conversions

The homepage visit example above is an extreme case, but the softer version is everywhere: scroll depth, time on page, PDF downloads, outbound link clicks — all marked as conversions because someone read a blog post about micro-conversions and got excited. These aren't meaningless metrics. They can be useful for understanding behavior. But they are not Google Ads conversions, and if you mark them as conversions, you've given the algorithm a very confused instruction.

The algorithm will do exactly what you told it to do. That's the problem.

## The Most Important Thing in This Article

Bad tracking is worse than no tracking. I want to be direct about this.

If you attach no tracking to your Google Ads account, the algorithm flies blind. That's bad — you'll get suboptimal bidding, your cost per lead will be higher than it should be, and you won't have the data to make good decisions. But the account will still function.

If you attach *wrong* tracking — if you tell the algorithm that homepage visits are conversions, or that your thank-you page is loading 400 times a day when it's really loading 40 — the algorithm optimizes aggressively for the wrong signal. It might actually get *worse* over time as it doubles down on what you've taught it. You'll spend money, see "conversions," make confident decisions, and get nowhere. Probably get somewhere negative.

This is why I tell people: **if you genuinely don't know how to set it up correctly, attach nothing until you do.** Don't slap something on because you know you're supposed to have tracking. A clean account with no conversion data is a better starting point than an account trained on bad conversion data. You can always add tracking later. You cannot easily undo six months of the algorithm learning from garbage inputs.

This is not a "do it later" item. Fix your tracking before you scale spend. Full stop.

## A Quick Note on Calls Specifically

I keep coming back to this because most businesses skip it. **Track your calls.**

You can set up call tracking through Google Ads natively — it swaps in a Google forwarding number on your site, and when someone calls it, a conversion fires in Google Ads. Takes about ten minutes to set up (see [the tracking setup library](/tracking) for the walkthrough).

Calls are frequently your highest-intent traffic. Someone searched, clicked your ad, read your page, decided they wanted to talk to a real person, and dialed. That's a warm lead. If that conversion isn't being recorded, the algorithm doesn't know that searcher turned into a qualified contact — it just sees a click that didn't lead to a form fill and treats it accordingly. You're misattributing your best leads.

## What the Rest of Your Tracking Stack Should Look Like

GA4 sits underneath all of this and records everything — page views, scroll depth, button clicks, all the behavioral stuff. That's fine. GA4 is your analytics layer. Let it collect whatever you want.

Google Ads conversions are a separate thing. The Google Ads pixel (also installed via GTM) only cares about the actions you've designated as conversions. Those should be form fills, calls, and offline conversions if you have them. That's the list.

Meta pixel, also inside GTM, follows the same logic — fire on meaningful actions. If you're running Meta ads alongside Google, you want the same event discipline there.

The [tracking setup library](/tracking) has individual guides broken out by form type, platform, and setup scenario. Use them.

## Diagnosing What's Wrong With Yours

If you're not sure whether your current tracking is right, the quickest path to an answer is [the 30-minute audit checklist](/ads/google-ads-account-audit-checklist). The tracking section will tell you exactly what to look for and what the red flags are.

If you're already doing weekly account maintenance, the [Google Ads weekly SOP](/ads/google-ads-sop-small-business) includes a tracking health check as part of the regular cadence. Tracking issues surface faster when you're looking at the account consistently.

And if you've already looked and you know something is off — your numbers feel wrong, your CPAs are either suspiciously great or suspiciously terrible, you're getting "conversions" but no actual leads — the most likely cause is [one of the common tracking mistakes covered here](/ads/google-ads-not-converting-fixes).

## When to Get Help

If you're not confident in your GTM setup, get someone who knows what they're doing to build it once, correctly. This is not an area to learn on the job with live ad spend running.

A bad tracking setup isn't just an annoyance — it actively corrupts the algorithm's model of your business. The longer it runs, the more work it takes to undo. I've audited accounts where the tracking had been wrong for a year and the bidding strategy had learned thoroughly from bad data. Getting those accounts back to a clean state took weeks of careful data rehabilitation, not just a quick fix.

Get it right the first time. Use the [tracking setup guides](/tracking) for the step-by-step. If you want a second set of eyes on what you've got, the audit is the fastest way to find out whether your current setup is trustworthy.

---

**Tired of guessing whether your ads are working?**

We manage Google and Meta ad accounts for businesses spending $500-$10,000/month. $800 setup, $200/month ongoing. You keep your account — we just make it work.

[→ Get a free account audit](/contact)

---
