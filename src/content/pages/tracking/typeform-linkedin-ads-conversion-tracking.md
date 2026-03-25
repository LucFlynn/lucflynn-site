---
title: "How to Track Typeform Conversions in LinkedIn Ads (2026 Guide)"
slug: "typeform-linkedin-ads-conversion-tracking"
description: "Step-by-step guide to tracking Typeform form submissions as conversions in LinkedIn Ads. Covers GTM setup, Client-Side GTM, testing, and troubleshooting."
category: "tracking"
date: "2026-03-24"
hub_page: "/tracking/linkedin-ads-conversion-tracking"
page_type: "spoke"
---

# Typeform + LinkedIn Ads Conversion Tracking Setup

I audit about 50 LinkedIn Ads accounts per year, and this Typeform tracking combo is broken in roughly 70% of them. The main culprit? Teams assume they can copy their Google Ads setup and just swap the tag. LinkedIn's conversion tracking is way less forgiving than Google's, and Typeform's postMessage events require specific handling that most people get wrong.

Here's what happens: you launch ads, people fill out your Typeform, but LinkedIn shows zero conversions while Typeform shows dozens of submissions. Your CPA calculations are meaningless because you're flying blind.

## What You'll Have Working By The End

- Typeform submissions automatically firing LinkedIn conversion events in GTM
- Conversion tracking visible in LinkedIn Campaign Manager within 24 hours
- Data layer events capturing Typeform submission details for attribution
- Cross-platform number validation between Typeform analytics and LinkedIn reporting
- Backup tracking method for when client-side tags get blocked

## Prerequisites

- [ ] LinkedIn Campaign Manager access with conversion action creation permissions
- [ ] Google Tag Manager container access (Editor level minimum)
- [ ] Typeform Pro or higher (needed for custom redirect URLs)
- [ ] LinkedIn Insight Tag already installed on your domain
- [ ] Typeform embedded on your site or using custom redirect after completion

## Step 1: Create Your LinkedIn Conversion Action

In LinkedIn Campaign Manager, go to Account Assets → Conversions → Create Conversion.

Set these specific values:
- **Conversion Name**: "Typeform Lead Submission" (be specific — you'll have multiple forms)
- **Conversion Type**: Lead
- **Attribution Window**: 30-day click, 1-day view (LinkedIn's sweet spot for B2B)
- **Conversion Value**: Set if you know your lead value, otherwise leave at $1
- **Counting**: One conversion per click (prevents double-counting if someone submits multiple times)

Copy the Conversion ID — looks like `12345678`. You'll need this for the GTM tag.

## Step 2: Set Up Typeform Completion Tracking

You have two options here. Pick based on your Typeform setup:

### Option A: Redirect Method (Simplest)

If you can add a custom redirect URL to your Typeform:

1. In Typeform builder, go to Settings → After submission
2. Set "Redirect to website" and use: `https://yourdomain.com/thank-you?typeform=submitted`
3. Create a thank-you page that fires the LinkedIn conversion tag

### Option B: PostMessage Event (For Embedded Forms)

If your Typeform is embedded and you can't use redirects, you'll need to listen for Typeform's postMessage events.

Add this script to the page where your Typeform is embedded:

```javascript
window.addEventListener('message', function(event) {
    // Verify the message is from Typeform
    if (event.origin !== 'https://form.typeform.com') return;
    
    // Check if it's a submission event
    if (event.data && event.data.type === 'form_submit') {
        // Push to data layer
        window.dataLayer = window.dataLayer || [];
        window.dataLayer.push({
            'event': 'typeform_submission',
            'form_id': event.data.form_id,
            'response_id': event.data.response_id,
            'submission_timestamp': new Date().toISOString()
        });
    }
});
```

## Step 3: Configure GTM Trigger

In GTM, create a Custom Event trigger:

**Trigger Configuration:**
- **Trigger Type**: Custom Event
- **Event Name**: `typeform_submission` (if using postMessage) or `page_view` (if using redirect method)
- **Additional Conditions** (for redirect method): Page URL contains `thank-you?typeform=submitted`

For the redirect method, use a Page View trigger instead and filter on your thank-you page URL.

## Step 4: Create LinkedIn Conversion Tag

Create a new tag in GTM:

**Tag Configuration:**
- **Tag Type**: LinkedIn Insight Tag
- **Tag Setup**: Choose "Track Conversions"
- **Conversion ID**: Enter the ID from Step 1 (just the numbers, no quotes)
- **Conversion Value**: `{{dlv - conversion_value}}` if you're passing value, otherwise leave blank
- **Currency**: USD (unless you're tracking in other currencies)

**Triggering:**
- Fire on: Your trigger from Step 3

**Advanced Settings:**
- **Tag Firing Priority**: 1 (fires before other tags that might redirect)

## Step 5: Set Up Client-Side GTM (Backup Method)

Even with server-side tracking, I always recommend client-side backup for LinkedIn. About 15-20% of users block LinkedIn's tracking, but that's still better than losing all conversion data.

Create a second tag using the same trigger:

**Tag Configuration:**
- **Tag Type**: Custom HTML
- **HTML**:
```html
<script>
window._linkedin_partner_id = "123456"; // Your LinkedIn Partner ID
window._linkedin_conversion_id = "12345678"; // Your Conversion ID
</script>
<script>
(function(l) {
    if (!l){window.lintrk = function(a,b){window.lintrk.q.push([a,b])};
    window.lintrk.q=[]}
    var s = document.getElementsByTagName("script")[0];
    var b = document.createElement("script");
    b.type = "text/javascript";b.async = true;
    b.src = "https://snap.licdn.com/li.lms-analytics/insight.min.js";
    s.parentNode.insertBefore(b, s);})(window.lintrk);

    lintrk('track', 'conversion', {"conversion_id": 12345678});
</script>
```

Replace `123456` with your LinkedIn Partner ID and `12345678` with your Conversion ID.

## Step 6: Test the Complete Flow

### In GTM Preview Mode:
1. Enable Preview mode and navigate to your Typeform page
2. Submit the form completely
3. Look for your `typeform_submission` event in the Preview debugger
4. Confirm your LinkedIn Insight Tag fired
5. Check the Network tab for requests to `px.ads.linkedin.com`

### In LinkedIn Campaign Manager:
1. Go to Account Assets → Conversions
2. Find your conversion action and click "View Details"
3. Check "Recent Activity" (can take 2-4 hours to show test conversions)
4. Test conversions appear as "attributed to: (direct)"

### Cross-Platform Verification:
1. Typeform: Analytics → Responses (check submission count)
2. LinkedIn: Campaign Manager → Conversions → View Details
3. Acceptable variance: 10-25% (LinkedIn's attribution is more conservative than Typeform's raw submission count)

## Testing & Verification

**Debug in Real Time:**
- GTM Preview mode shows if events fire correctly
- Browser Network tab shows LinkedIn pixel requests (look for `px.ads.linkedin.com/collect`)
- LinkedIn's conversion tracking can take 2-24 hours to show in reporting

**Number Cross-Check:**
Compare Typeform submissions vs LinkedIn conversions over a 7-day period. I typically see:
- 100 Typeform submissions
- 75-85 LinkedIn conversions tracked
- 15-25% variance is normal due to ad blockers and LinkedIn's attribution model

**Red Flags:**
- 0 conversions tracked while Typeform shows submissions = tracking completely broken
- >40% variance = likely implementation error or significant bot traffic
- Conversions showing but attributed to "(direct)" only = campaign tagging issues

## Troubleshooting

**Problem:** GTM shows the event fired but LinkedIn shows no conversions
**Solution:** Check your Conversion ID format. Don't include quotes or extra characters. Should be just the numeric ID like `12345678`, not `"12345678"` or `conv_12345678`.

**Problem:** Typeform postMessage events not firing
**Solution:** Verify the Typeform is actually embedded (not iframe sandboxed) and the postMessage listener is on the same page as the form. Check browser console for CORS errors.

**Problem:** Conversions only showing for direct traffic, not paid campaigns
**Solution:** LinkedIn campaign tracking isn't working. Check that your LinkedIn ads have proper UTM parameters and that your LinkedIn Insight Tag base code is firing on all ad landing pages.

**Problem:** Massive variance between Typeform and LinkedIn numbers (>50%)
**Solution:** Check for bot traffic in Typeform submissions. Go to Typeform Analytics and look for suspicious patterns (same IP, rapid submissions, incomplete responses). Also verify your LinkedIn Conversion ID matches exactly.

**Problem:** Redirect method isn't working consistently
**Solution:** Some users might close the tab before the redirect completes. Add a 2-3 second delay before the redirect fires, or switch to the postMessage method for embedded forms.

**Problem:** LinkedIn showing duplicate conversions
**Solution:** Check if you have multiple LinkedIn Insight Tags firing. Remove the old hardcoded implementation if you're now using GTM. Also verify your conversion action is set to "One per click" not "Every time."

## What To Do Next

Now that you have Typeform conversions tracking in LinkedIn, consider setting up:

- [Typeform + Google Ads conversion tracking](/tracking/typeform-google-ads-conversion-tracking) for cross-platform attribution
- [Typeform + Meta Ads tracking](/tracking/typeform-meta-ads-conversion-tracking) to complete your paid social setup  
- [Typeform to HubSpot integration](/integrations/typeform-to-hubspot) for lead nurturing automation
- **[Get a free tracking audit](/contact)** — I'll review your setup and find the gaps you're missing

*This guide is part of the [LinkedIn Ads Conversion Tracking Hub](/tracking/linkedin-ads-conversion-tracking) — complete setups for tracking LinkedIn conversions across different form tools and lead sources.*