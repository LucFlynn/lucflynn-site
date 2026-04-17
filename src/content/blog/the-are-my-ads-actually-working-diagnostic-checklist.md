---
title: "The 'Are My Ads Actually Working?' Diagnostic Checklist"
description: "**I've audited over 200 Google Ads accounts in the last eight years, and I'd estimate 85% of them have at least four of these problems.** Most business..."
pubDate: 2026-04-17
topic: "Google Ads"
seo_keywords: "ads, checklist, actually, working', diagnostic, 'are"
draft: false
---

# The "Are My Ads Actually Working?" Diagnostic Checklist

**I've audited over 200 Google Ads accounts in the last eight years, and I'd estimate 85% of them have at least four of these problems.** Most business owners don't even know they're bleeding money because the platforms make everything look fine on the surface.

The client calls are always the same. "The ads aren't working." I pull up their account and see decent click-through rates, reasonable cost per clicks, leads flowing in. Then I dig deeper and find conversion tracking that's been broken for six months, or campaigns optimizing for page views instead of actual sales, or attribution windows set up to make Meta look like a hero while Google gets zero credit.

**This checklist is for business owners who are spending $2,000+ per month on ads and want to know if their money is actually driving results.** If you're seeing leads but not customers, if your cost per acquisition keeps climbing, or if you inherited an ad account that "someone else set up," keep reading.

I've organized this into the exact order I use when auditing accounts. Start at the top. The further down the list your problems go, the more money you're probably wasting.

## Foundation: Conversion Tracking (Check These First)

**1. Your conversion tracking is actually firing**
Open Google Ads, go to Tools & Settings > Conversions. Check if you have any conversions recorded in the last 30 days. If the answer is zero, or if the numbers look suspiciously round (exactly 100, exactly 50), your tracking is broken. Good looks like: messy numbers that match your actual business results. I've seen accounts "optimizing" for months with zero conversion data.

**2. You're tracking the right actions**
Look at what you're counting as conversions. Page views of a thank-you page? Wrong. Newsletter signups on a lead-gen business? Wrong. For lead generation, you should track exactly two things: form submissions and phone calls. For e-commerce: purchases and high-intent actions like "add to cart" (but weight purchases 10x higher). If you're tracking more than four conversion actions, you're tracking too many.

**3. Duplicate conversions aren't inflating your numbers**
Check if your thank-you page redirects to itself on form errors. Check if you have both Google Ads conversion tracking AND Google Analytics goals firing on the same action. Check if your Meta pixel and Google tag are both counting the same purchase. I found a client last month where every failed form submission was counting as a conversion because their developer set up the tracking wrong. Real conversion rate: 3%. Reported conversion rate: 47%.

**4. Your attribution windows make sense**
In Google Ads, go to Tools & Settings > Attribution. If you're running lead generation, your conversion window should be 30 days maximum. If you're running e-commerce with a long consideration cycle, maybe 90 days. If it's set to "data-driven" and you have less than 3,000 conversions in 30 days, switch to "last click" — you don't have enough data for Google's model to work.

**5. Enhanced Conversions is configured properly**
Go to your conversion action and check if Enhanced Conversions shows "Eligible" or "Not set up." If it's not set up, you're missing 10-30% of your conversions due to privacy restrictions and cookie blocking. This isn't optional anymore in 2025. The setup requires your developer to pass customer emails and phone numbers to Google in a hashed format.

## Campaign Structure: The Money Bleed

**6. Your campaigns have clear, single purposes**
Open your campaign list. Each campaign should target one product/service, one geographic area, one customer type. If you have campaigns called "General Keywords" or "Brand + Competitors," that's a red flag. Good looks like: "Chicago Personal Injury - Auto Accidents" not "Legal Services - All Practice Areas." Mixed-intent campaigns waste money on irrelevant clicks.

**7. Your ad groups are tightly themed**
Click into any campaign. Your ad groups should contain 5-20 keywords maximum, all variations of the same search intent. If you have ad groups with 50+ keywords covering different topics, you're showing irrelevant ads to qualified traffic. I see this constantly — one ad group trying to cover "bankruptcy lawyers," "divorce lawyers," and "estate planning attorneys" with the same ad copy.

**8. You're not running Performance Max without conversion data**
If you have Performance Max campaigns (the black box campaigns that run across all of Google), check how many conversions they've driven in the last 30 days. If it's under 30, pause them immediately. Performance Max needs conversion volume to learn. Without it, you're just paying Google to show your ads to anyone, anywhere. I've seen accounts burn $5,000/month on Performance Max with zero conversions.

**9. Your negative keyword lists aren't ancient**
Go to Tools & Settings > Negative keyword lists. Check when they were last updated. If you imported a negative keyword list from 2019 and never touched it, you're probably blocking your own ads from showing. I found a client blocking the word "services" as a negative keyword, which prevented their service-based business from appearing for any relevant searches.

## Keywords and Targeting: Control What You Can

**10. You're not relying on broad match for everything**
Check your keyword match types. If 80%+ of your keywords are broad match, you're letting Google decide who sees your ads instead of controlling it yourself. Start with exact match and phrase match. Add broad match only after you have conversion data proving what works. I've seen broad match campaigns trigger for "epoxy epoxy" when the client sold commercial floor coatings.

**11. Your search terms report tells a coherent story**
Go to Keywords > Search terms. Look at what people actually searched for when they clicked your ads. If you see irrelevant searches, DIY searches for a commercial service, or complete gibberish, your keywords are too broad. Add negative keywords immediately. Good looks like: search terms that are obvious variations of what you sell.

**12. Your audience targeting isn't fighting itself**
If you're running Display, YouTube, or Performance Max campaigns, check your audience settings. "Observation" means you're watching but not restricting. "Targeting" means you're only showing to those audiences. If you have both demographic targeting AND interest targeting AND custom audiences all set to "targeting," you're probably reaching nobody.

## Landing Pages and User Experience

**13. Your ads send people to relevant pages**
Click through your own ads. Do they land on your homepage? That's wrong. Do they land on a page that matches the search intent? That's right. If someone searches "emergency roof repair Chicago" and lands on your general roofing services page, they're bouncing. Every campaign should have dedicated landing pages that match the ad copy and keyword intent.

**14. Your forms work on mobile**
Check your conversion rate by device in Google Ads. If mobile converts 50%+ worse than desktop, your forms are probably broken on phones. Test your lead forms on multiple devices. If they're hard to fill out, require too much information, or don't work with autofill, you're losing qualified leads.

**15. Your phone tracking captures everything**
If you're a local business, check if your phone number changes when people click from Google Ads. It should — that's call tracking. If your phone number is the same whether someone comes from organic search or paid ads, you have no idea how many people are calling because of your advertising. You're flying blind on 30-50% of your conversions.

## Platform-Specific Gotchas

**16. Your Google and Meta attribution windows are aligned**
Check your attribution settings in both platforms. If Google is using 30-day attribution and Meta is using 7-day, they're crediting different conversions and you can't compare performance. I like 30-day click, 1-day view for both platforms. Anything longer and you're crediting ads for conversions that would have happened anyway.

**17. Your Meta pixel is firing server-side**
In Meta Events Manager, check if your pixel events show "Server" or "Browser" as the connection method. If it's all browser events, you're losing 20-30% of conversions to iOS privacy restrictions and ad blockers. Server-side setup requires technical work but it's not optional anymore if you want accurate data.

**18. You're not optimizing for landing page views**
Check your Meta campaign objectives. If any campaign is optimizing for "Landing Page Views" instead of actual conversions, change it immediately. Landing page views is a fake metric that makes Meta's numbers look good while burning your budget on people who bounce.

## Advanced Tracking and Attribution

**19. Your server-side tracking is actually working**
If you've set up server-side Google Tag Manager, go to your server container and check if events are firing in real-time mode. If you see zero events or if events stopped firing weeks ago, your server-side setup is broken and you're back to losing conversion data. This requires a developer to fix.

**20. You have backup attribution beyond platform reporting**
The platforms lie. Not on purpose, but they each want credit for every conversion. Check if you have a third-party attribution tool like Triple Whale, Northbeam, or Hyros running alongside your platform pixels. If you're only looking at Google and Meta dashboards, you're making decisions based on incomplete data.

## Scoring Your Account Health

**1-4 issues:** Minor tune-up needed. You're probably wasting 10-15% of your spend on fixable problems.

**5-9 issues:** You're likely wasting 25-40% of your budget. This is costing you real money every month.

**10+ issues:** Stop running ads until you fix these foundational problems. You're burning money, not investing it.

## What This Checklist Can't Catch

This diagnostic catches the obvious stuff — the broken tracking, the wasteful keywords, the basic setup errors that bleed money every day. But the stuff that really kills ROI is harder to spot in a self-audit.

Attribution gaps between platforms. Tracking drift over time. Audience decay in long-running campaigns. Bid strategy conflicts. Campaign cannibalization. The technical setup that looks right but performs wrong.

That's what a professional audit covers. It's the difference between stopping the bleeding and actually optimizing for growth.

I charge $800 for a complete account audit because it takes me 6-8 hours to check everything properly. But this checklist will catch 80% of the problems for free. Start here. Fix what you can. If you're still not seeing the results you need, then we should talk.

---

*Want the PDF version of this checklist? [Download it here](https://electroraven.com/checklist) — it includes the specific steps to fix each issue.*
