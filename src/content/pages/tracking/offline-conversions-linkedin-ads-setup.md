---
title: "Offline Conversion Import for LinkedIn Ads: Complete Setup Guide (2026)"
slug: "offline-conversions-linkedin-ads-setup"
description: "Complete guide to setting up Offline Conversion Import for LinkedIn Ads. Step-by-step configuration, testing, and troubleshooting."
category: "tracking"
date: "2026-03-24"
hub_page: "/tracking/offline-conversions"
page_type: "spoke"
---

# Offline Conversion Import + LinkedIn Ads Setup Guide

I see broken offline conversion setups for LinkedIn in about 60% of B2B accounts I audit. Usually it's missing the LinkedIn Click ID in the initial tracking, or they're trying to match on email when LinkedIn's match rates are terrible for anything that's not a direct form fill.

LinkedIn's offline conversion import is different from Facebook and Google — they're pickier about data freshness (conversions older than 90 days get rejected), and their matching logic heavily favors the LinkedIn Click ID over hashed emails.

## What You'll Have Working By The End

- LinkedIn Click ID capturing on all ad traffic and storing it with your lead data
- Automated offline conversion uploads to LinkedIn via their API
- Conversion attribution showing in LinkedIn Campaign Manager within 24-48 hours
- Match rates above 70% (vs. the 15-25% most setups get with email-only matching)
- Proper conversion deduplication to avoid inflated numbers

## Prerequisites

- [ ] LinkedIn Campaign Manager access (Campaign Manager or Account Manager role)
- [ ] LinkedIn Marketing Developer Platform app created and approved
- [ ] Server-side infrastructure to store click IDs and process conversions (Cloud Run, AWS Lambda, or similar)
- [ ] CRM or database that can store the LinkedIn Click ID with lead records
- [ ] GTM container with Enhanced Conversions setup (if using GTM for click ID capture)

## Architecture Overview

Here's how the data flows:

1. **Click Capture**: User clicks LinkedIn ad → LinkedIn Click ID gets captured and stored with session
2. **Form Submission**: User converts → Click ID gets attached to conversion record in your CRM
3. **Conversion Processing**: Your server processes the conversion → Formats data for LinkedIn API
4. **Upload**: Batch upload to LinkedIn Conversions API → Conversions appear in Campaign Manager

The critical piece most setups miss: capturing and persisting the LinkedIn Click ID (`li_fat_id`) from the initial ad click through to the final conversion record.

## Step 1: Capture LinkedIn Click IDs

LinkedIn appends the Click ID as `li_fat_id` in the URL parameters. You need to capture this on page load and store it.

**Option A: GTM Setup**

Create a URL variable in GTM:
- Variable Type: URL
- Component Type: Query
- Query Key: `li_fat_id`

Then create a trigger for all LinkedIn traffic and fire a tag to store the Click ID in a cookie or session storage:

```javascript
// Custom HTML tag in GTM
<script>
function storeLinkedInClickId() {
    var liClickId = {{LinkedIn Click ID Variable}}; // Your GTM variable
    if (liClickId) {
        // Store in cookie (expires in 30 days)
        document.cookie = "li_click_id=" + liClickId + ";path=/;max-age=2592000;SameSite=Lax";
        
        // Also store in sessionStorage for immediate access
        sessionStorage.setItem('li_click_id', liClickId);
    }
}
storeLinkedInClickId();
</script>
```

**Option B: Server-Side Capture**

If you're using server-side GTM or direct server tracking:

```javascript
// Node.js example
app.get('*', (req, res, next) => {
    const liClickId = req.query.li_fat_id;
    if (liClickId) {
        // Store in session or database
        req.session.li_click_id = liClickId;
        
        // Set cookie for client-side access
        res.cookie('li_click_id', liClickId, {
            maxAge: 30 * 24 * 60 * 60 * 1000, // 30 days
            httpOnly: false,
            sameSite: 'lax'
        });
    }
    next();
});
```

## Step 2: Attach Click ID to Conversion Records

When users convert, you need to grab the stored LinkedIn Click ID and associate it with the conversion in your CRM.

**Form Submission Handler:**

```javascript
// On form submit
document.getElementById('leadForm').addEventListener('submit', function(e) {
    // Get stored LinkedIn Click ID
    const liClickId = getCookie('li_click_id') || sessionStorage.getItem('li_click_id');
    
    if (liClickId) {
        // Add as hidden field or send with form data
        const hiddenField = document.createElement('input');
        hiddenField.type = 'hidden';
        hiddenField.name = 'linkedin_click_id';
        hiddenField.value = liClickId;
        this.appendChild(hiddenField);
    }
});

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}
```

Make sure your CRM integration captures this LinkedIn Click ID field and stores it with the lead record.

## Step 3: Set Up LinkedIn Conversions API

First, create a conversion rule in LinkedIn Campaign Manager:
1. Go to Analyze → Conversion Tracking
2. Create New Conversion
3. Select "Offline" as the tracking method
4. Note the Conversion Rule ID — you'll need this for the API

**API Authentication:**

```javascript
// Get access token (OAuth 2.0)
const getAccessToken = async () => {
    const response = await fetch('https://www.linkedin.com/oauth/v2/accessToken', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
            'grant_type': 'client_credentials',
            'client_id': process.env.LINKEDIN_CLIENT_ID,
            'client_secret': process.env.LINKEDIN_CLIENT_SECRET,
            'scope': 'w_member_social,rw_ads'
        })
    });
    
    const data = await response.json();
    return data.access_token;
};
```

## Step 4: Upload Offline Conversions

**Batch Upload Function:**

```javascript
const uploadConversions = async (conversions, accessToken) => {
    const payload = {
        "elements": conversions.map(conversion => ({
            "conversion": {
                "campaignId": conversion.campaign_id, // Optional, for campaign-level attribution
                "creativeId": conversion.creative_id,   // Optional, for creative-level attribution
                "conversionHappenedAt": conversion.timestamp, // Unix timestamp in milliseconds
                "conversionValue": {
                    "currencyCode": "USD",
                    "amount": conversion.value.toString()
                },
                "eventType": "LEAD", // or "PURCHASE", "SIGN_UP", etc.
                "userIdentifiers": {
                    "linkedinFirstPartyAdsTrackingUUIDs": [conversion.linkedin_click_id]
                }
            }
        }))
    };

    const response = await fetch(`https://api.linkedin.com/rest/conversions?ids=List(urn:li:sponsoredConversionRule:${CONVERSION_RULE_ID})`, {
        method: 'POST',
        headers: {
            'Authorization': `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
            'LinkedIn-Version': '202301',
            'X-Restli-Protocol-Version': '2.0.0'
        },
        body: JSON.stringify(payload)
    });

    return await response.json();
};
```

**Data Quality Requirements:**

- `conversionHappenedAt`: Must be within 90 days, Unix timestamp in milliseconds
- `linkedinFirstPartyAdsTrackingUUIDs`: The LinkedIn Click ID (`li_fat_id`) is critical for match rates
- `conversionValue`: Optional but recommended for ROAS tracking
- Upload frequency: I recommend batching uploads every 4-6 hours for faster attribution

## Step 5: Testing & Verification

**Test in LinkedIn Campaign Manager:**

1. Go to Analyze → Conversion Tracking
2. Select your conversion rule
3. Check "Test Events" tab to see recent uploads
4. Verify match status — "Matched" means LinkedIn successfully attributed the conversion

**Debug API Response:**

```javascript
// Check API response for errors
const result = await uploadConversions(testConversions, accessToken);

if (result.errors) {
    console.error('Upload errors:', result.errors);
    // Common errors:
    // - "INVALID_LINKEDIN_FIRST_PARTY_ADS_TRACKING_UUID" = bad click ID format
    // - "CONVERSION_TOO_OLD" = conversion older than 90 days
    // - "INVALID_CURRENCY_CODE" = currency not supported
}

console.log('Uploaded conversions:', result.elements?.length || 0);
```

**Match Rate Verification:**

Check your match rates in Campaign Manager after 24-48 hours:
- **Good**: 70%+ match rate (with LinkedIn Click ID)
- **Poor**: 15-25% match rate (email-only matching)
- **Broken**: <5% match rate (something's wrong with your setup)

## Troubleshooting

**Problem**: LinkedIn Click ID not capturing → Check URL parameters on LinkedIn ad traffic. The Click ID appears as `li_fat_id` in the query string.

**Problem**: Conversions uploading but not matching → Your LinkedIn Click ID is probably corrupted or not the original value. Don't URL decode it — send it exactly as captured from the ad click.

**Problem**: API returning "INVALID_CONVERSION_RULE" → Double-check your Conversion Rule ID in the API endpoint URL. It should be a numeric ID, not the rule name.

**Problem**: Match rates dropping over time → Click IDs expire after LinkedIn's attribution window (default 30 days). Make sure you're not uploading conversions with stale Click IDs.

**Problem**: Duplicate conversions showing → LinkedIn doesn't automatically dedupe. You need to implement deduplication on your end before uploading, or use unique external IDs in the API payload.

**Problem**: Campaign Manager showing "Processing" status for days → This usually means your conversion timestamps are in the wrong format. Use Unix milliseconds, not seconds: `Date.now()` not `Math.floor(Date.now()/1000)`.

## What To Do Next

- Set up [Facebook Offline Conversions](/tracking/offline-conversions-facebook-ads-setup) to track the same leads across platforms
- Implement [Google Ads Offline Conversion Import](/tracking/offline-conversions-google-ads-setup) for complete cross-platform attribution  
- Configure [Enhanced Conversions](/tracking/enhanced-conversions) to improve match rates on your other platforms
- **Get a free tracking audit**: [Contact me](/contact) to review your current offline conversion setup and identify gaps

*This guide is part of the [Offline Conversion Import Hub](/tracking/offline-conversions) — complete guides for tracking offline conversions across all major ad platforms.*